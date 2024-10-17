from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from constance import config

User._meta.get_field("email")._unique = True


class Course(models.Model):
    code = models.TextField()
    name = models.TextField()

    def __str__(self):
        return f"[{self.code}] {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code"], name="course_code_unique")
        ]
        indexes = [models.Index(fields=["code"], name="course_code_index")]


class College(models.Model):
    name = models.TextField()
    city = models.TextField()
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    college_type = models.TextField()
    code = models.TextField()
    programs = models.ManyToManyField(Course, through="Program")
    # By default, max length of slug field is 50, which causes error in Postgres
    slug = models.SlugField(max_length=255)

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code"], name="college_code_unique")
        ]
        indexes = [models.Index(fields=["code"], name="college_code_index")]

    def save(self, *args, **kwargs):
        # Doesn't matter if the URL changes, since the application does not care
        # about the slug part of the url.
        self.slug = slugify(self.name)
        super(College, self).save(*args, **kwargs)


class RankList(models.Model):
    short_name = models.TextField()
    name = models.TextField()

    def __str__(self) -> str:
        return f"[{self.short_name}] {self.name}"

    class Meta:
        indexes = [models.Index(fields=["short_name"])]


class Program(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_seats = models.PositiveIntegerField()
    ranklist = models.ForeignKey(RankList, on_delete=models.RESTRICT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["college", "course"],
                name="course_cannot_be_repeated_in_college",
            )
        ]
        indexes = [models.Index(fields=["college", "course"])]

    def __str__(self) -> str:
        return f"{self.college.code}_{self.course.code} {self.total_seats:03} {self.ranklist.short_name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    # Last time the user updated their choices
    last_choice_save_date = models.DateTimeField(default=timezone.now)
    last_choice_report_generation_date = models.DateTimeField(null=True, blank=True)
    choice_report_path = models.TextField(null=True, blank=True, default='')
    
    # Whether this student can add new programs to their choice list
    choice_entry_add_new_programs_allowed = models.BooleanField(default=True)
    # Whether choice entry has been disabled for this user
    choice_entry_disabled = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return f"{self.user.id} {self.user.get_full_name()}"


class RankListEntry(models.Model):
    ranklist = models.ForeignKey(RankList, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rank = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ranklist", "student"], name="student_unique_in_ranklist"
            )
        ]

    def __str__(self) -> str:
        return f"{self.ranklist.short_name} {self.student} {self.rank}"

class Round(models.Model):
    number = models.IntegerField()
    name = models.TextField()

    def __str__(self) -> str:
        return f"[{self.number}] {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number"], name="round_number_unique"
            )
        ]


class ChoiceEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "program", "round"], name="student_program_round_unique"
            )
        ]

    def __str__(self) -> str:
        return f"[{self.round.number}] {self.student} {self.program} {self.priority}"
    
    def save(self, *args, **kwargs):
        self.round = Round.objects.get(number=config.CURRENT_ROUND)
        super(ChoiceEntry, self).save(*args, **kwargs)




class Allotment(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(
        Program, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["round", "student"], name="round_student_unique"
            )
        ]
