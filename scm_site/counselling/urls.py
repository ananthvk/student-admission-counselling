from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("college/<int:college_id>/", views.college_detail, name="college_detail"),
    path("college/list/", views.CollegeListView.as_view(), name="college_list"),
]
