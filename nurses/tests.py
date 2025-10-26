# nurses/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class NursePatientViewSetTestCase(TestCase):
    """
    Tests for NursePatientViewSet:
    - Only nurses can access patient list.
    - Non-nurses should be denied.
    - Search filter should work.
    """

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.nurse_user = User.objects.create_user(
            username="nurse1",
            email="nurse1@example.com",
            password="password123",
            role="nurse"
        )

        self.non_nurse_user = User.objects.create_user(
            username="doctor1",
            email="doctor1@example.com",
            password="password123",
            role="doctor"
        )

        self.patient1 = User.objects.create_user(
            username="patientA",
            email="patientA@example.com",
            password="password123",
            role="patient"
        )

        self.patient2 = User.objects.create_user(
            username="patientB",
            email="patientB@example.com",
            password="password123",
            role="patient"
        )

        # API endpoint
        self.url = reverse('nursepatient-list')  # name from DefaultRouter (e.g. router.register('nurse-patients', ...))

    def test_nurse_can_view_patients(self):
        """Nurse should be able to list all patients"""
        self.client.force_authenticate(user=self.nurse_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        usernames = [patient["username"] for patient in results]
        self.assertIn("patientA", usernames)
        self.assertIn("patientB", usernames)

    def test_non_nurse_cannot_view_patients(self):
        """Non-nurses should be denied access"""
        self.client.force_authenticate(user=self.non_nurse_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_denied(self):
        """Unauthenticated users should be denied access"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_filter(self):
        """Nurse can filter patients by username"""
        self.client.force_authenticate(user=self.nurse_user)
        response = self.client.get(self.url, {'search': 'patientA'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        usernames = [patient["username"] for patient in results]
        self.assertIn("patientA", usernames)
        self.assertNotIn("patientB", usernames)
