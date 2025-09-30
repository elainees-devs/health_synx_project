# patients/models.py
from django.db import models
from django.conf import settings

# ---------------------------------------------------------
# Patient
# ---------------------------------------------------------
# Extends the User model with patient-specific information.
# - Links to the User model via a one-to-one relationship.
# - Stores full name, date of birth, gender, contact, and medical history.
class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        unique=True
    )
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
