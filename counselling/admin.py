from django.contrib import admin
from preferences.admin import PreferencesAdmin
from .models import Course, College, ChoiceEntry, Program, RankList, RankListEntry, Student, SitePreference
# Register your models here.

admin.site.register(Course)
admin.site.register(College)
admin.site.register(ChoiceEntry)
admin.site.register(Program)
admin.site.register(RankList)
admin.site.register(RankListEntry)
admin.site.register(Student)

admin.site.register(SitePreference, PreferencesAdmin)