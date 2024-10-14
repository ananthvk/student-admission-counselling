from ..tasks import perform_allotment_da
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import (
    College,
    Course,
    Program,
    Student,
    RankList,
    RankListEntry,
    ChoiceEntry,
    Round,
    Allotment,
)
from constance import config
import json


class TasksTestCase(TestCase):
    def setUp(self):
        self.ranklist = RankList.objects.create(short_name="RL", name="A rank list")
        self.round = Round.objects.create(number=1, name="First round")

        # Create 10 students
        self.students = []
        for i in range(10):
            student = Student(
                user=User.objects.create_user(
                    username=f"testuser{i}",
                    password="password",
                    email=f"test{i}@testuser.com",
                ),
                date_of_birth="2003-01-01",
            )
            student.save()
            self.students += [student]

            # Add the student to the ranklist
            RankListEntry.objects.create(
                ranklist=self.ranklist, student=student, rank=(i + 1)
            )

        # Helpers for tests which uses only a single instance
        self.college = College.objects.create(code=f"E001", name=f"First college")
        self.course = Course.objects.create(code="CS", name="Computer Science")
        self.course2 = Course.objects.create(code="IS", name="Info Science")

        self.program = Program.objects.create(
            college=self.college,
            course=self.course,
            total_seats=5,
            ranklist=self.ranklist,
        )

        self.program2 = Program.objects.create(
            college=self.college,
            course=self.course2,
            total_seats=5,
            ranklist=self.ranklist,
        )

        self.student = self.students[0]

    def test_allotment_single_ranklist_single_college_single_program(self):
        ChoiceEntry.objects.create(
            student=self.student, program=self.program, priority=1
        )
        perform_allotment_da()
        self.assertEqual(Allotment.objects.count(), len(self.students))
        for student in self.students[1:]:
            self.assertIsNone(Allotment.objects.get(round=self.round, student=student).program, None)
        self.assertEqual(Allotment.objects.get(round=self.round, student=self.student).program, self.program)
    
    def test_allotment_with_two_programs(self):
        ChoiceEntry.objects.create(student=self.student, program=self.program, priority=1)
        ChoiceEntry.objects.create(student=self.students[1], program=self.program2, priority=1)

        perform_allotment_da()

        self.assertEqual(Allotment.objects.get(round=self.round, student=self.student).program, self.program)

        self.assertEqual(Allotment.objects.get(round=self.round, student=self.students[1]).program, self.program2)

    def test_allotment_priority_system(self):
        ChoiceEntry.objects.create(student=self.student, program=self.program2, priority=2)
        ChoiceEntry.objects.create(student=self.student, program=self.program, priority=1)

        perform_allotment_da()

        self.assertEqual(Allotment.objects.get(round=self.round, student=self.student).program, self.program)


    def test_no_available_seats(self):
        self.program.total_seats = 0
        self.program.save()

        ChoiceEntry.objects.create(student=self.student, program=self.program, priority=1)

        perform_allotment_da()

        self.assertIsNone(Allotment.objects.get(round=self.round, student=self.student).program)

    def test_multiple_students_no_seats_available(self):
        for student in self.students:
            ChoiceEntry.objects.create(student=student, program=self.program, priority=1)

        perform_allotment_da()
        
        for i, student in enumerate(self.students):
            allotment = Allotment.objects.get(round=self.round, student=student)
            if i < 5:
                self.assertEqual(allotment.program, self.program)
            else:
                self.assertIsNone(allotment.program)