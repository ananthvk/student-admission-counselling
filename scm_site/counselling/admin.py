from django.contrib import admin
from .models import Course, College, ChoiceEntry, Program, RankList, RankListEntry, Student
# Register your models here.

admin.site.register(Course)
admin.site.register(College)
admin.site.register(ChoiceEntry)
admin.site.register(Program)
admin.site.register(RankList)
admin.site.register(RankListEntry)
admin.site.register(Student)