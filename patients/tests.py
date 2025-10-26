# patients/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from patients.models import PatientProfile, PatientVitals, DoctorQueue


class PatientViewSetTestCase(APITestCase):
    """Tests for PatientViewSet actions."""

    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass", role="admin"
        )
        self.nurse_user = User.objects.create_user(
            username="nurse", password="nursepass", role="nurse"
        )
        self.doctor_user = User.objects.create_user(
            username="doctor", password="doctorpass", role="doctor"
        )
        self.patient_user = User.objects.create_user(
            username="patient", password="patientpass", role="patient"
        )

        # Create patient profile
        self.patient_profile = PatientProfile.objects.create(
            user=self.patient_user
        )

        # Sample vitals for patient
        self.vitals = PatientVitals.objects.create(
            patient=self.patient_user,
            temperature=37.2,
            pulse_rate=80,
        )

        # Doctor queue entry
        self.queue = DoctorQueue.objects.create(
            patient=self.patient_user,
            vitals=self.vitals,
            doctor=self.doctor_user,
            status="with_doctor",
        )

        self.list_url = reverse("patient-list")
        self.vitals_url = reverse("patient-vitals", args=[self.patient_user.id])
        self.record_vitals_url = reverse("patient-record-vitals", args=[self.patient_user.id])
        self.add_to_queue_url = reverse("patient-add-to-queue", args=[self.patient_user.id])
        self.send_to_pharmacy_url = reverse("patient-send-to-pharmacy", args=[self.queue.id])

    # ----------------------------------------------------------------------
    def test_unauthenticated_access_denied(self):
        """Ensure unauthenticated users cannot access endpoints."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------------------------------------------------------
    def test_nurse_can_record_vitals(self):
        """Nurse can record patient vitals and add them to doctor queue."""
        self.client.login(username="nurse", password="nursepass")
        payload = {"temperature": 36.8, "pulse_rate": 75}
        response = self.client.post(self.record_vitals_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Vitals recorded", response.data["message"])

    # ----------------------------------------------------------------------
    def test_doctor_can_view_vitals(self):
        """Doctor can view all recorded vitals for a patient."""
        self.client.login(username="doctor", password="doctorpass")
        response = self.client.get(self.vitals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # ----------------------------------------------------------------------
    def test_add_to_queue_without_vitals(self):
        """Should fail if patient has no vitals recorded."""
        # create a new patient without vitals
        new_patient = User.objects.create_user(username="no_vitals", password="123", role="patient")
        PatientProfile.objects.create(user=new_patient)

        self.client.login(username="nurse", password="nursepass")
        url = reverse("patient-add-to-queue", args=[new_patient.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No vitals", response.data["error"])

    # ----------------------------------------------------------------------
    def test_send_to_pharmacy_invalid_status(self):
        """Should fail if patient is not 'with_doctor'."""
        self.client.login(username="doctor", password="doctorpass")
        # create queue not in 'with_doctor' status
        queue = DoctorQueue.objects.create(
            patient=self.patient_user, vitals=self.vitals, doctor=self.doctor_user, status="waiting"
        )
        url = reverse("patient-send-to-pharmacy", args=[queue.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("must be with doctor", response.data["error"])
