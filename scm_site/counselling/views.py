from django.http import HttpResponse, HttpRequest
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from .models import College, Course

# Create your views here.


def index(request: HttpRequest):
    return render(request, "counselling/index.html", context={})


class CollegeListView(ListView):
    model = College
    # paginate_by = 100


class CourseListView(ListView):
    model = Course


class CollegeDetailView(DetailView):
    pk_url_kwarg = "college_id"
    slug_url_kwarg = "slug"
    model = College
