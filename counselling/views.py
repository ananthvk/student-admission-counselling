import json
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseForbidden,
    HttpResponse,
)
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.core.files.storage import default_storage
from django.db import transaction
from preferences import preferences
from django.core.cache import cache
from .tasks import generate_report_task
from .models import (
    College,
    Course,
    Program,
    Student,
    ChoiceEntry,
    RankListEntry,
)

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


@login_required
@ensure_csrf_cookie
def option_entry_view(request: HttpRequest):

    if not preferences.SitePreference.choice_entry_enabled:
        return render(request, "counselling/choice_entry_closed.html")

    # Only return those colleges which offer atleast one program
    queryset = (
        College.objects.filter(programs__isnull=False).distinct().order_by("code")
    )
    # Also pass in the options filled by this candidate, if they want to update it
    student = Student.objects.get(user=request.user)
    choices = ChoiceEntry.objects.filter(student=student).order_by("priority")
    return render(
        request,
        "counselling/choice_entry.html",
        {"colleges": queryset, "choices": choices},
    )


@login_required
@require_http_methods(["POST"])
def option_entry_post(request: HttpRequest):
    if not preferences.SitePreference.choice_entry_enabled:
        return HttpResponseForbidden("Choice entry has been closed")
    payload = json.loads(request.body)
    student = Student.objects.get(user=request.user)
    with transaction.atomic():
        college_ids = [i[1] for i in payload]
        course_ids = [i[2] for i in payload]

        ChoiceEntry.objects.filter(student=student).exclude(program__college_id__in=college_ids, program__course_id__in=course_ids).delete()

        for priority_number, college_id, course_id in payload:
            program = Program.objects.get(college_id=college_id, course_id=course_id)

            choice_entry, created = ChoiceEntry.objects.update_or_create(
               student=student, program=program,
               defaults={'priority': priority_number},
            )
        
        student.last_choice_save_date=timezone.now()
        student.save()
    
    # TODO: If the user hits save twice, two tasks are generated, discard the previous task
    # Generate the report when the student saves their choices, so that later it can be served directly
    task = generate_report_task.delay(request.user.pk)
    # Save the task_id and the user_id to the cache, so that the user cannot make multiple requests to generate the report
    cache.set(request.user.pk, task.id)
    return JsonResponse({"status": "ok"})


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


class RankListView(ListView):
    model = RankListEntry
    template_name = "counselling/rank_list.html"
    paginate_by = 100
    queryset = RankListEntry.objects.all().order_by("rank")
    context_object_name = "rank_list"


@login_required
def download_choice_report_view(request: HttpRequest):
    report_path = f'{request.user.username}_choice_report.pdf'
    task_id = cache.get(request.user.pk) 

    if not default_storage.exists(report_path):
        # Create a task to generate the report
        if task_id is None:
            task = generate_report_task.delay(request.user.pk)
            cache.set(request.user.pk, task.id)

        # A task is working on generating this user's report, do not create another task
        return HttpResponse("Your report is being generated, please wait for a while and then try again later")
    
    with default_storage.open(report_path) as report_file:
        response = HttpResponse(report_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="{report_path}"'
        )
        return response
