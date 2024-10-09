from django.http import (
    HttpRequest,
    JsonResponse,
    FileResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponse
)
import io
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
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import transaction
import json
from .reports import PreferenceListReport
from .tasks import generate_report_task
from preferences import preferences
from celery.result import AsyncResult

# Create your views here.


def index(request: HttpRequest):
    return render(request, "counselling/index.html", context={})


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

    return JsonResponse({"status": "ok"})


@require_http_methods(["GET"])
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
    task = generate_report_task.delay(request.user.pk)
    #result = io.BytesIO(task.get())
    #return FileResponse(
    #    result,
    #    as_attachment=False,
    #    filename=f"{request.user.username}_choice_report.pdf",
    #)
    return render(request, "counselling/download_choice_report.html", context={"task": task})
    

def get_task_status(request: HttpRequest, task_id):
    result = AsyncResult(task_id)
    task_result = {
        "task_id": task_id,
        "task_status": result.status,
    }

    return JsonResponse(task_result, status=200)

@login_required
def get_task_result(request: HttpRequest, task_id):
    result = AsyncResult(task_id)
    if result is None or result.result is None:
        return HttpResponseNotFound("Resource not found")
        
    if ('%s' % request.user.id) != ('%s' % result.result['user_id']):
        return HttpResponseNotFound("Resource not found")
    if result.status == 'SUCCESS':
            response = HttpResponse(result.result['pdf'], content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="report.pdf"'
            return response
    else:
        return JsonResponse({'error': 'Not yet ready'}, status=500)