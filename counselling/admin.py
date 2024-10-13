from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Course, College, ChoiceEntry, Program, RankList, RankListEntry, Student
# Register your models here.


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    pass

@admin.register(College)
class CollegeAdmin(ModelAdmin):
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
