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
from .models import (
    College,
    Course,
    Program,
    Student,
    ChoiceEntry,
    RankListEntry,
)
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.core.files.storage import default_storage
from django.db import transaction
import json
from .tasks import generate_report_task, perform_allotment_da
from preferences import preferences
from django.core.cache import cache

def index(request: HttpRequest):
    # perform_allotment_da.delay()
    return render(request, "counselling/index.html")

class CollegeListView(ListView):
    model = College
    ordering = "code"
    # paginate_by = 100



class CourseListView(ListView):
    model = Course


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

        # TODO: Delete all choices of the students before adding them again,
        # This is wasteful and inefficient, Implement deletion of only those ids which are not in the list
        ChoiceEntry.objects.filter(student=student).delete()

        for priority_number, college_id, course_id in payload:
            program = Program.objects.get(college_id=college_id, course_id=course_id)

            # choice_entry, created = ChoiceEntry.objects.update_or_create(
            #    student=student, program=program,
            #    defaults={'priority': priority_number},
            # )
            ChoiceEntry(
                student=student, program=program, priority=priority_number
            ).save()
        
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
