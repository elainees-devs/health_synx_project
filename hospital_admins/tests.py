# hospital_admins/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class HospitalAdminViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
            role="hospital_admin"
        )
        self.normal_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            role="patient"
        )
