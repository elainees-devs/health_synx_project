# hospital_admins/models.py
from django.db import models
from django.core.exceptions import ValidationError
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

    def clean(self):
        """Ensure that the user has role hospital_admin"""
        if self.user.user_role != 'hospital_admin': 
            raise ValidationError(f"User {self.user.email} is not a hospital_admin.")

    def save(self, *args, **kwargs):
        self.clean()  # validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        # Get user's full name
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return f"{full_name} ({self.user.role})"
