from django.contrib import admin
from unfold.admin import ModelAdmin
from preferences.admin import PreferencesAdmin
from .models import Course, College, ChoiceEntry, Program, RankList, RankListEntry, Student, SitePreference
# Register your models here.


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    pass

@admin.register(College)
class CollegeAdmin(ModelAdmin):
    pass

@admin.register(ChoiceEntry)
class ChoiceEntryAdmin(ModelAdmin):
    pass

@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    pass

@admin.register(RankList)
class RankListAdmin(ModelAdmin):
    pass

@admin.register(RankListEntry)
class RankListEntryAdmin(ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(ModelAdmin):
    pass

admin.site.register(SitePreference, PreferencesAdmin)
class PreferencesAdminClass(ModelAdmin):
    pass