from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from .models import College, Course
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


# Create your views here.


def index(request: HttpRequest):
    return render(request, "counselling/index.html", context={})


class CollegeListView(ListView):
    model = College
    ordering = 'code'
    # paginate_by = 100

class CourseListView(ListView):
    model = Course


class CollegeDetailView(DetailView):
    pk_url_kwarg = "college_id"
    slug_url_kwarg = "slug"
    model = College

@login_required
def option_entry_view(request: HttpRequest):
    queryset = College.objects.all().order_by("code")
    return render(request, "counselling/choice_entry.html", {"colleges": queryset})

@require_http_methods(["GET"])
def get_programs_offered_by_college(request: HttpRequest, college_id):
    #program_codes = get_object_or_404(College, pk=college_id).programs.order_by('code').values('code')
    program_codes = get_object_or_404(College, pk=college_id).programs.order_by('code')
    return JsonResponse({x.code:x.name for x in program_codes})