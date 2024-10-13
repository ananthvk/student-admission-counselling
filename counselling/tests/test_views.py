from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import (
    College,
    Course,
    Program,
    Student,
    RankList,
    ChoiceEntry,
    RankListEntry,
)
from constance import config
import json


class CounsellingViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.student = Student.objects.create(
            user=self.user, date_of_birth="2003-01-01"
        )

        self.courses = []
        self.colleges = []
        self.programs = []
        self.ranklist = RankList.objects.create(
            short_name="ENG_RL", name="Engineering rank list"
        )

        for i in range(10):
            self.colleges.append(
                College.objects.create(
                    code=f"E00{i}", name=f"Test college of engineering {i}"
                )
            )

        for i in range(10, 30):
            self.courses.append(
                Course.objects.create(code=f"{i}", name=f"{i*10} Subject")
            )

        for i in range(10):
            self.programs.append(
                Program.objects.create(
                    college=self.colleges[i],
                    course=self.courses[i],
                    total_seats=5,
                    ranklist=self.ranklist,
                )
            )
            self.programs.append(
                Program.objects.create(
                    college=self.colleges[i],
                    course=self.courses[i + 10],
                    total_seats=10,
                    ranklist=self.ranklist,
                )
            )

        self.college = College.objects.create(
            name="ABCD College of Engineering",
            city="Bengaluru",
            address="XYZ Street, LMN Road",
            college_type="ENGG",
            code="E999",
        )
        for course in self.courses:
            Program.objects.create(
                college=self.college,
                course=course,
                total_seats=50,
                ranklist=self.ranklist,
            )

    def test_index_view(self):
        response = self.client.get(reverse("counselling:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "counselling/index.html")
        self.assertTrue(b"available courses" in response.content)
        self.assertTrue(b"login" in response.content)

    def test_college_list_view(self):
        response = self.client.get(reverse("counselling:college_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["college_list"]), 11)
        self.assertTrue(b"E001" in response.content)
        self.assertTrue(b"Test college of engineering 1" in response.content)

    def test_course_list_view(self):
        response = self.client.get(reverse("counselling:course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["course_list"]), 20)
        self.assertTrue(b"10" in response.content)
        self.assertTrue(b"100 Subject" in response.content)

    def test_college_detail_view(self):
        response = self.client.get(
            reverse(
                "counselling:college_detail", kwargs={"college_id": self.college.id}
            )
        )
        txt = response.content.decode("utf-8")
        self.assertTrue(self.college.name, txt)
        self.assertTrue(self.college.code, txt)
        self.assertTrue(self.college.city, txt)

    def test_choice_entry_view_redirects_if_not_authenticated(self):
        response = self.client.get(reverse("counselling:choice_entry"))
        self.assertEqual(response.status_code, 302)

    def test_choice_entry_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("counselling:choice_entry"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "counselling/choice_entry.html")

    def test_choice_entry_post(self):
        self.client.login(username="testuser", password="password")
        payload = [[1, self.college.id, self.courses[0].id]]
        response = self.client.post(
            reverse("counselling:choice_entry_post"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChoiceEntry.objects.count(), 1)

    def test_choice_entry_post_choice_entry_closed(self):
        self.client.login(username="testuser", password="password")
        config.CHOICE_ENTRY_ENABLED = False
        payload = [[1, self.college.id, self.courses[0].id]]
        response = self.client.post(
            reverse("counselling:choice_entry_post"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertTrue(b'Choice entry has been closed' in response.content)
        self.assertEqual(response.status_code, 403)