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
    path("rank/", views.view_ranks, name="view_ranks"),
    path("ranklist/", views.RankListView.as_view(), name="ranklist_view"),
    path("api/choiceentry", views.option_entry_post, name="choice_entry_post"),
    path("api/college/<int:college_id>/programs", views.get_programs_offered_by_college, name="get_programs_offered_by_college"),
    path("download_choice_report/", views.download_choice_report_view, name="download_choice_report"),
    path("tasks/<str:task_id>/status", views.get_task_status, name="get_task_status"),
    path("tasks/<str:task_id>/pdf", views.get_task_result, name="get_task_result")
]
