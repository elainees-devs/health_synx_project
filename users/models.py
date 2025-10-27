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

    PATIENT_TYPE_CHOICES = [
        ('inpatient', 'Inpatient'),
        ('outpatient', 'Outpatient'),
    ]

    GENDER_CHOICES=[
        ('male', 'Male'),
        ('female', 'Female'),
    ]


    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')

    # Avoid circular import by using string reference
    department = models.ForeignKey(
        'departments.Department',   
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    # only relevant if role == 'patient'
    patient_type = models.CharField(
        max_length=20,
        choices=PATIENT_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Select whether the patient is an inpatient or outpatient."
    )

    def __str__(self):
        dept_info = f" - {self.department.name}" if self.department else ""
        return f"{self.username} ({self.role}){dept_info}"

    class Meta:
        indexes = [
            models.Index(fields=['role']),
        ]
        ordering = ['id']  # Order by id ascending
