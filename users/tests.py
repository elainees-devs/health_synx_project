# users/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from users.models import User

User = get_user_model()


class UsersViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create users with correct role field
        self.doctor = User.objects.create_user(username='doc1', password='password123', role='doctor')
        self.nurse = User.objects.create_user(username='nurse1', password='password123', role='nurse')
        self.admin = User.objects.create_user(username='admin1', password='password123', role='hospital_admin')
        self.patient = User.objects.create_user(username='patient1', password='password123', role='patient')

    # -----------------------------
    # Test registration (requires hospital admin)
    # -----------------------------
    def test_register_user(self):
        self.client.force_login(self.admin)  # Must be hospital admin
        url = reverse('register_patient')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpass123",
            "role": "patient",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Patient registered successfully!", response.data["message"])

    # -----------------------------
    # Test login
    # -----------------------------
    def test_login_user(self):
        url = reverse('login')
        data = {"username": "doc1", "password": "password123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "doc1")

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {"username": "doc1", "password": "wrongpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid username/email or password", response.data["error"])

    # -----------------------------
    # Test logout
    # -----------------------------
    def test_logout_user(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")

    # -----------------------------
    # Test redirect after login
    # -----------------------------
    def test_redirect_after_login_doctor(self):
        self.client.force_login(self.doctor)
        url = reverse('redirect_after_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Compare against reverse() path
        self.assertEqual(response.url, reverse('doctor_dashboard'))

    # -----------------------------
    # Test Doctor Dashboard
    # -----------------------------
    def test_doctor_dashboard_access(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('doctor_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_patients", response.data)
        self.assertIn("queue", response.data)
        # Optional: check that patient info uses username
        for q in response.data["queue"]:
            self.assertIn("patient__username", q or q.get("patient_name"))

    # -----------------------------
    # Test Nurse Dashboard
    # -----------------------------
    def test_nurse_dashboard_access(self):
        self.client.force_authenticate(user=self.nurse)
        url = reverse('nurse_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Welcome Nurse! Dashboard ready.")

    # -----------------------------
    # Test Hospital Admin Dashboard
    # -----------------------------
    def test_admin_dashboard_access(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('hospital_admin_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("departments", response.data)
        self.assertIn("staff_count", response.data)
