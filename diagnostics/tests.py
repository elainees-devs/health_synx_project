# diagnostics/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import get_user_model

from diagnostics.models import LabTest, LabQueue, XRay, XRayQueue, MRI, MRIQueue
from users.models import User

User = get_user_model()

class DiagnosticsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a patient
        self.patient = User.objects.create_user(
            username='patient1', password='password123', role='patient',
            first_name='John', last_name='Doe'
        )

        # Create a technician
        self.technician = User.objects.create_user(
            username='tech1', password='password123', role='technician',
            first_name='Tech', last_name='One'
        )

        # Authenticate as technician
        self.client.force_authenticate(user=self.technician)

        # Create sample LabTest, XRay, MRI
        self.lab_test = LabTest.objects.create(name='Complete Blood Count')
        self.xray_test = XRay.objects.create(name='Chest X-Ray')
        self.mri_test = MRI.objects.create(name='Brain MRI')

        # Create queues
        self.lab_queue = LabQueue.objects.create(
            patient=self.patient, lab_test=self.lab_test, technician=self.technician
        )
        self.xray_queue = XRayQueue.objects.create(
            patient=self.patient, xray=self.xray_test, technician=self.technician
        )
        self.mri_queue = MRIQueue.objects.create(
            patient=self.patient, mri=self.mri_test, technician=self.technician
        )

    @patch('diagnostics.views.create_diagnostic_fee')
    def test_complete_lab_queue(self, mock_fee):
        url = reverse('lab-queue-complete', args=[self.lab_queue.id])
        response = self.client.post(url, {'results': 'All normal'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lab_queue.refresh_from_db()
        self.assertEqual(self.lab_queue.status, 'completed')
        self.assertEqual(self.lab_queue.results, 'All normal')
        mock_fee.assert_called_once_with(self.patient, self.lab_queue, test_type='lab')

    def test_complete_lab_queue_missing_results(self):
        url = reverse('lab-queue-complete', args=[self.lab_queue.id])
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('diagnostics.views.create_diagnostic_fee')
    def test_complete_xray_queue(self, mock_fee):
        url = reverse('xray-queue-complete', args=[self.xray_queue.id])
        response = self.client.post(url, {'results': 'Fracture detected'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.xray_queue.refresh_from_db()
        self.assertEqual(self.xray_queue.status, 'completed')
        self.assertEqual(self.xray_queue.results, 'Fracture detected')
        mock_fee.assert_called_once_with(self.patient, self.xray_queue, test_type='xray')

    def test_complete_xray_queue_missing_results(self):
        url = reverse('xray-queue-complete', args=[self.xray_queue.id])
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('diagnostics.views.create_diagnostic_fee')
    def test_complete_mri_queue(self, mock_fee):
        url = reverse('mri-queue-complete', args=[self.mri_queue.id])
        response = self.client.post(url, {'results': 'No abnormalities'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mri_queue.refresh_from_db()
        self.assertEqual(self.mri_queue.status, 'completed')
        self.assertEqual(self.mri_queue.results, 'No abnormalities')
        mock_fee.assert_called_once_with(self.patient, self.mri_queue, test_type='mri')

    def test_complete_mri_queue_missing_results(self):
        url = reverse('mri-queue-complete', args=[self.mri_queue.id])
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
