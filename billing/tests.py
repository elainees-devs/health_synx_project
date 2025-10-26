# billing/test.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from billing.models import BillingRecord
from django.http import HttpResponse

User = get_user_model()

class BillingRecordViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a billing user
        self.billing_user = User.objects.create_user(
            username='billing1', password='password123', role='billing'
        )

        # Create a patient
        self.patient = User.objects.create_user(
            username='patient1', password='password123', role='patient',
            first_name='John', last_name='Doe'
        )

        # Create Billing Records
        self.record1 = BillingRecord.objects.create(
            patient=self.patient,
            category='consultation',
            amount=100,
            paid=False
        )
        self.record2 = BillingRecord.objects.create(
            patient=self.patient,
            category='lab',
            amount=200,
            paid=True
        )

        # Authenticate billing user
        self.client.force_authenticate(user=self.billing_user)

    def test_list_billing_records(self):
        url = reverse('billing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patient_full_name = f"{self.patient.first_name} {self.patient.last_name}"
        records_for_patient = [
            r for r in response.data['results']  # <-- use 'results' for paginated response
            if r['patient_name'] == patient_full_name
        ]
        self.assertEqual(len(records_for_patient), 2)

    def test_retrieve_billing_record(self):
        url = reverse('billing-detail', args=[self.record1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patient_full_name = f"{self.patient.first_name} {self.patient.last_name}"
        self.assertEqual(response.data['patient_name'], patient_full_name)

    def test_mark_paid_billing_record(self):
        url = reverse('billing-mark-paid', args=[self.record1.id])

        # Mock render_to_pdf to return a real HttpResponse
        import billing.views as views
        from unittest.mock import patch

        with patch.object(views, 'render_to_pdf', return_value=HttpResponse(b"PDF")):
            response = self.client.post(url)
            self.record1.refresh_from_db()
            self.assertTrue(self.record1.paid)
            self.assertEqual(response.status_code, 200)

    def test_totals_billing_records(self):
        url = reverse('billing-totals')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('grand_total', response.data)
        self.assertEqual(response.data['grand_total'], 300)
        self.assertIn('category_totals', response.data)
