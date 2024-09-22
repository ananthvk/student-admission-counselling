from django.http import HttpResponse, HttpRequest
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from .models import College

# Create your views here.


def index(request: HttpRequest):
    return HttpResponse("Hello world")


class CollegeListView(ListView):
    model = College
    # paginate_by = 100


def college_detail(request: HttpRequest, college_id):
    college = get_object_or_404(College, pk=college_id)
    return render(request, "counselling/college_detail.html", context={"college": college})
