import json
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseForbidden,
    HttpResponse,
    HttpResponseNotFound
)
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.cache import cache_page
from django.core.files.storage import default_storage
from django.db import transaction
from django.core.cache import cache
from .tasks import generate_report_task, perform_allotment_da
from .models import (
    College,
    Course,
    Program,
    Student,
    ChoiceEntry,
    RankListEntry,
    Allotment,
    Round,
)
from constance import config
from scm_site.celery import app

"""
This view is the home page for the application, it shows some links related to counselling
such as choice entry, view ranks, etc.
"""


def index(request: HttpRequest):
    return render(request, "counselling/index.html")


"""
This view lists the colleges which are available, along with a link to view detailed information about the college.
"""


class CollegeListView(ListView):
    model = College
    ordering = "code"


"""
This view lists all courses which are offered by the colleges, along with their course code.
"""


class CourseListView(ListView):
    model = Course


"""
This view displays detailed information about a particular college, also has a slug field 
"""


class CollegeDetailView(DetailView):
    pk_url_kwarg = "college_id"
    slug_url_kwarg = "slug"
    model = College

    def get_queryset(self):
        return (
            College.objects.prefetch_related("program_set", "program_set__course")
            .all()
            .order_by("code")
        )


"""
This view displays the choice entry page, where a student can add, modify or reorder their preference list.
"""


@login_required
@ensure_csrf_cookie
def choice_entry_view(request: HttpRequest):

    if not config.CHOICE_ENTRY_ENABLED:
        return render(
            request, "counselling/choice_entry_closed.html", context={"message": ""}
        )

    student = Student.objects.get(user=request.user)

    if student.choice_entry_disabled:
        return render(
            request,
            "counselling/choice_entry_closed.html",
            context={"message": "You are not allowed to modify your choices further"},
        )

    # Only return those colleges which offer atleast one program
    queryset = (
        College.objects.filter(programs__isnull=False).distinct().order_by("code")
    )
    # Also pass in the options filled by this candidate, if they want to update it

    # Avoid the N+1 problem by using select_related so that Django performs a join instead of creating multiple queries
    choices = (
        ChoiceEntry.objects.select_related(
            "program", "program__college", "program__course"
        )
        .filter(student=student)
        .order_by("priority")
    )
    return render(
        request,
        "counselling/choice_entry.html",
        {"colleges": queryset, "choices": choices},
    )


@login_required
@require_http_methods(["POST"])
def choice_entry_post(request: HttpRequest):

    student = Student.objects.get(user=request.user)

    if not config.CHOICE_ENTRY_ENABLED or student.choice_entry_disabled:
        return HttpResponseForbidden("Choice entry has been closed")

    payload = json.loads(request.body)
    college_ids = [i[1] for i in payload]
    course_ids = [i[2] for i in payload]

    with transaction.atomic():

        ChoiceEntry.objects.filter(student=student).exclude(
            program__college_id__in=college_ids, program__course_id__in=course_ids
        ).delete()

        for priority_number, college_id, course_id in payload:
            program = Program.objects.get(college_id=college_id, course_id=course_id)

            choice_entry, created = ChoiceEntry.objects.update_or_create(
                student=student,
                program=program,
                defaults={"priority": priority_number},
            )

        student.last_choice_save_date = timezone.now()
        student.save()

    # If a task is generating the report for the student, stop it
    task_id = cache.get(request.user.pk)
    if task_id is not None:
        app.control.revoke(task_id, terminate=True)
        cache.delete(request.user.pk)

    return JsonResponse({"status": "ok"})


"""
This view returns all courses offered by a college as JSON, this is used by the choice entry view.
"""


@require_http_methods(["GET"])
@cache_page(settings.TIMEOUT)
def get_programs_offered_by_college(request: HttpRequest, college_id):
    # program_codes = get_object_or_404(College, pk=college_id).programs.order_by('code').values('code')
    program_codes = get_object_or_404(College, pk=college_id).programs.order_by("code")
    return JsonResponse(
        {
            "courses": [
                {"id": x.id, "code": x.code, "name": x.name} for x in program_codes
            ]
        }
    )


@require_http_methods(["GET"])
@login_required
def view_ranks(request: HttpRequest):
    ranklist_entries = RankListEntry.objects.filter(student=request.user.student)
    return render(
        request,
        "counselling/view_ranks.html",
        context={"ranklist_entries": ranklist_entries},
    )


@login_required
def view_allotment(request: HttpRequest):
    if not config.SHOW_ALLOTMENT_RESULTS:
        return HttpResponseForbidden("Allotment results are not yet published")

    student: Student = request.user.student
    round: Round = Round.objects.get(number=config.CURRENT_ROUND)
    try:
        allotment = Allotment.objects.select_related(
            "program", "program__course", "program__college"
        ).get(student=student, round=round)
    except ObjectDoesNotExist:
        allotment = None
    return render(
        request,
        "counselling/view_allotment.html",
        context={"round": round, "allotment": allotment},
    )


class RankListView(ListView):
    model = RankListEntry
    template_name = "counselling/rank_list.html"
    paginate_by = 100
    queryset = RankListEntry.objects.all().order_by("rank")
    context_object_name = "rank_list"

    def get_queryset(self):
        # Avoid the N+1 problem by using select_related
        return (
            RankListEntry.objects.select_related("student", "student__user")
            .all()
            .order_by("rank")
        )


from logging import getLogger

logger = getLogger(__name__)


@login_required
def download_choice_report_view(request: HttpRequest):
    student: Student = request.user.student
    report_path = student.choice_report_path
    task_id = cache.get(request.user.pk)

    # A task is working on generating this user's report, do not create another task
    if task_id is not None:
        return HttpResponse(
            "Your report is being generated, please wait for a while and then try again later"
        )

    # If The student has not generated any report, or
    # If the choices were updated, generate a new report
    # Or if the report was deleted
    if (
        student.last_choice_report_generation_date is None
        or student.last_choice_save_date > student.last_choice_report_generation_date
        or (
            student.choice_report_path
            and not default_storage.exists(student.choice_report_path)
        )
    ):
        task = generate_report_task.delay(request.user.pk)
        cache.set(request.user.pk, task.id)
        return HttpResponse(
            "Your report is being generated, please wait for a while and then try again later"
        )

    #with default_storage.open(report_path) as report_file:
    #    response = HttpResponse(report_file, content_type="application/pdf")
    #    response["Content-Disposition"] = f'inline; filename="{report_path}"'
    #    return response
    return redirect(f"{settings.MEDIA_URL}{report_path}")


"""
Various actions: Such as allotment, other tasks for the superuser
"""
@login_required
@requires_csrf_token
def actions_view(request: HttpRequest):
    if not request.user.is_superuser:
        return HttpResponseNotFound("Not found")
    
    if request.method == 'POST':
        if cache.get("allotment-task") is not None:
            return HttpResponse(f'Allotment task is already running....please wait until the task completes')
        cache.set("allotment-task", "created")
        task = perform_allotment_da.delay()
        return HttpResponse(f'Created task for allotment {task.id}')
    else:
        return render(request, "counselling/actions_view.html")
        