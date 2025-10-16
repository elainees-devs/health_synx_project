# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('pharmacist', 'Pharmacist'),
        ('lab_tech', 'Lab Technician'),
        ('imaging_tech', 'Imaging Technician'),
        ('billing', 'Billing Officer'),
        ('nurse', 'Nurse'),
        ('hospital_admin', 'Hospital Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    class Meta:
        indexes = [
            models.Index(fields=['role']),  # Index on role for faster lookups
        ]
