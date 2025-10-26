# departments/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from departments.models import Department

User = get_user_model()

class DepartmentViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin1', password='password123', role='admin'
        )

        # Create a hospital admin user
        self.hospital_admin_user = User.objects.create_user(
            username='hospital_admin1', password='password123', role='hospital_admin'
        )

        # Create a normal user (should not have access)
        self.normal_user = User.objects.create_user(
            username='user1', password='password123', role='doctor'
        )

        # Create some departments
        self.department1 = Department.objects.create(name='Cardiology', description='Heart dept')
        self.department2 = Department.objects.create(name='Neurology', description='Brain dept')

        # URLs
        self.list_url = reverse('department-list')  # DRF router names

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_list_departments(self):
        self.authenticate(self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # check results list


    def test_retrieve_department(self):
        self.authenticate(self.admin_user)
        url = reverse('department-detail', args=[self.department1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.department1.name)

    def test_create_department_as_admin(self):
        self.authenticate(self.admin_user)
        data = {'name': 'Pediatrics', 'description': 'Children dept'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'Pediatrics')

    def test_create_department_as_hospital_admin(self):
        self.authenticate(self.hospital_admin_user)
        data = {'name': 'Oncology', 'description': 'Cancer dept'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'Oncology')

    def test_create_department_as_normal_user_forbidden(self):
        self.authenticate(self.normal_user)
        data = {'name': 'Oncology', 'description': 'Cancer dept'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_department(self):
        self.authenticate(self.admin_user)
        url = reverse('department-detail', args=[self.department1.id])
        data = {'description': 'Updated description'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department1.refresh_from_db()
        self.assertEqual(self.department1.description, 'Updated description')

    def test_delete_department(self):
        self.authenticate(self.admin_user)
        url = reverse('department-detail', args=[self.department2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(id=self.department2.id).exists())
