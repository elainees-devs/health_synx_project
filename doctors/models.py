# doctors/models.py
from django.db import models

from users.models import User
from departments.models import Department

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    # Work-related details
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors'
    )

    def __str__(self):
        # Get doctor's full name
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return f"{full_name} ({self.user.role})"
