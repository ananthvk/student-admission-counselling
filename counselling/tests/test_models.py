from django.test import TestCase
from ..models import College

class CollegeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        College.objects.create(name="XYZ college", city="ABC", address="123, Lane")

    def test_slug_is_generated(self):
        self.assertIsNotNone(College.objects.first().slug)
        self.assertGreater(len(College.objects.first().slug), 0)