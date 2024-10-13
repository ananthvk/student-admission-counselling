from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Course, College, ChoiceEntry, Program, RankList, RankListEntry, Student, Round
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

@admin.register(Round)
class RoundAdmin(ModelAdmin):
    pass

from constance.admin import ConstanceAdmin, Config
from constance.forms import ConstanceForm
class CustomConfigForm(ConstanceForm):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #... do stuff to make your settings form nice ...

class ConfigAdmin(ConstanceAdmin, ModelAdmin):
    change_list_form = CustomConfigForm
    change_list_template = 'admin/config/settings.html'

admin.site.unregister([Config])
admin.site.register([Config], ConstanceAdmin)
