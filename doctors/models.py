# doctors/models.py
from django.db import models
from django.core.exceptions import ValidationError
from users.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)

    def clean(self):
        # Enforce that only users with the doctor role can be assigned
        if self.user.role != 'doctor':
            raise ValidationError("The linked user must have the role 'doctor'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # run validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"
