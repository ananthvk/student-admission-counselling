from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from .models import College, Course, Program, Student, ChoiceEntry
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import transaction
import json

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
    # Only return those colleges which offer atleast one program
    queryset = (
        College.objects.filter(programs__isnull=False).distinct().order_by("code")
    )
    # Also pass in the options filled by this candidate, if they want to update it
    student = Student.objects.get(user=request.user)
    choices = ChoiceEntry.objects.filter(student=student).order_by("priority")
    return render(request, "counselling/choice_entry.html", {"colleges": queryset, "choices": choices})


@login_required
@require_http_methods(["POST"])
def option_entry_post(request: HttpRequest):
    payload = json.loads(request.body)
    student = Student.objects.get(user=request.user)
    with transaction.atomic():
        for priority_number, college_id, course_id in payload:
            program = Program.objects.get(college_id=college_id, course_id=course_id)
            choice_entry = ChoiceEntry(student=student, program=program, priority=priority_number)
            choice_entry.save()
        
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
