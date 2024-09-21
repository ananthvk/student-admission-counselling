from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.

def index(request: HttpRequest):
    return HttpResponse("Hello world")