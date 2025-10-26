# doctors/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from patients.models import DoctorQueue, DoctorNote, Prescription, PrescriptionItem, PatientVitals
from pharmacy.models import Medicine
from doctors.models import DoctorProfile


User = get_user_model()


class DoctorsSetupMixin:
    """Mixin to create common test data"""

    def setUp(self):
        # Create a doctor user
        self.doctor = User.objects.create_user(
            username="drsmith",
            email="drsmith@example.com",
            password="password123",
            role="doctor"
        )

        # Create DoctorProfile linked to this user
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.doctor,
            specialization="General Medicine",
            license_number="DOC-001"
        )

        # Create a patient user
        self.patient = User.objects.create_user(
            username="johndoe",
            email="johndoe@example.com",
            password="password123",
            role="patient"
        )

        # Create patient vitals (required by DoctorQueue)
        self.vitals = PatientVitals.objects.create(
            patient=self.patient,
            temperature=36.6,
            pulse_rate=72
        )

        # Create DoctorQueue
        self.queue = DoctorQueue.objects.create(
            patient=self.patient,
            vitals=self.vitals,
            status="waiting"
        )

        # Create a medicine
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            description="Pain relief",
            price=10.0
        )

        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.doctor)
class DoctorQueueViewSetTestCase(DoctorsSetupMixin, APITestCase):
    def test_list_doctor_queue(self):
        url = reverse("doctor-queue-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get("results", [])
        self.assertTrue(len(data) >= 1)

    def test_waiting_queue(self):
        url = reverse("doctor-queue-waiting")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get("results", [])
        self.assertTrue(any(item["status"] == "waiting" for item in data))

    def test_update_queue_status(self):
        url = reverse("doctor-queue-update-status", args=[self.queue.id])
        response = self.client.post(url, {"status": "with_doctor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.queue.refresh_from_db()
        self.assertEqual(self.queue.status, "with_doctor")


class DoctorNoteViewSetTestCase(DoctorsSetupMixin, APITestCase):
    def test_create_doctor_note(self):
        url = reverse("doctor-note-list")
        response = self.client.post(url, {
            "patient": self.patient.id,
            "queue_item": self.queue.id,
            "diagnosis": "Patient is stable."
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Handle doctor being blank, nested, or ID
        doctor_field = response.data.get("doctor")
        if isinstance(doctor_field, dict):
            self.assertEqual(doctor_field.get("id"), self.doctor.id)
        elif doctor_field in [None, "", " "]:
            note = DoctorNote.objects.last()
            self.assertEqual(note.doctor, self.doctor)
        else:
            self.assertIn(str(self.doctor.id), str(doctor_field))


class PrescriptionViewSetTestCase(DoctorsSetupMixin, APITestCase):
    def setUp(self):
        super().setUp()
        # Create a prescription
        self.prescription = Prescription.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            queue_item=self.queue
        )

    def test_add_prescription_items(self):
        url = reverse("prescription-add-items", args=[self.prescription.id])
        response = self.client.post(url, {
            "medicine_id": [self.medicine.id],
            "dosage": ["2 tablets"]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["dosage"], "2 tablets")

        # Ensure the queue status updated
        self.queue.refresh_from_db()
        self.assertEqual(self.queue.status, "sent_to_pharmacy")


class DoctorViewSetTestCase(DoctorsSetupMixin, APITestCase):
    def test_list_doctors(self):
        url = reverse("doctor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data if isinstance(response.data, list) else response.data.get("results", [])
        self.assertGreaterEqual(len(data), 1)

        first = data[0]
        # Handle serializer variations
        if "user" in first:
            self.assertEqual(first["user"]["id"], self.doctor.id)

        elif "id" in first:
            self.assertEqual(first["id"], self.doctor.id)
        elif "username" in first:
            self.assertEqual(first["username"], self.doctor.username)
