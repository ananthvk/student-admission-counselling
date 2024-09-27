from django.urls import path
from . import views

app_name = "counselling"
urlpatterns = [
    path("", views.index, name="index"),
    path("college/<int:college_id>/", views.CollegeDetailView.as_view(), name="college_detail"),
    path("college/<int:college_id>/<slug:slug>", views.CollegeDetailView.as_view(), name="college_detail"),
    path("college/list/", views.CollegeListView.as_view(), name="college_list"),
    path("course/list/", views.CourseListView.as_view(), name="course_list"),
    path("choiceentry/", views.option_entry_view, name="choice_entry"),
    path("api/college/<int:college_id>/programs", views.get_programs_offered_by_college)
]
