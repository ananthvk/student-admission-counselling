from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.TextField()
    code = models.TextField()


class College(models.Model):
    name = models.TextField()
    address = models.TextField()
    contact_email = models.EmailField()
    college_type = models.TextField()
    code = models.TextField()
    programs = models.ManyToManyField(Course, through="Program")


class RankList(models.Model):
    short_name = models.TextField()
    name = models.TextField()


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


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()


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


class ChoiceEntry(models.Model):
    priority = models.IntegerField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "program"], name="student_program_unique"
            )
        ]
