# hospital_admins/models.py
from django.db import models
from users.models import User
from departments.models import Department

class HospitalAdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Work-related details
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hospital_admins'
    )

    def __str__(self):
        # Get user's full name
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return f"{full_name} ({self.user.role})"
