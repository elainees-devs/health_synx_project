# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# ---------------------------------------------------------
# User
# ---------------------------------------------------------
# Custom User model extending Django's AbstractUser.
# - Adds role-based access with predefined ROLES.
# - Includes additional fields: email, phone_number, date_of_birth.
# - Tracks creation and update timestamps.
class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
