from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.conf import settings
CACHE_TTL = settings.TIMEOUT

app_name = "counselling"
urlpatterns = [
    path("", views.index, name="index"),
    path("college/<int:college_id>/", cache_page(CACHE_TTL)(views.CollegeDetailView.as_view()), name="college_detail"),
    path("college/<int:college_id>/<slug:slug>", cache_page(CACHE_TTL)(views.CollegeDetailView.as_view()), name="college_detail"),
    path("college/list/", cache_page(CACHE_TTL)(views.CollegeListView.as_view()), name="college_list"),
    path("course/list/", cache_page(CACHE_TTL)(views.CourseListView.as_view()), name="course_list"),
    path("ranklist/", cache_page(CACHE_TTL)(views.RankListView.as_view()), name="ranklist_view"),
    path("choiceentry/", views.option_entry_view, name="choice_entry"),
    path("rank/", views.view_ranks, name="view_ranks"),
    path("api/choiceentry", views.option_entry_post, name="choice_entry_post"),
    path("api/college/<int:college_id>/programs", views.get_programs_offered_by_college, name="get_programs_offered_by_college"),
    path("download_choice_report/", views.download_choice_report_view, name="download_choice_report"),
]
