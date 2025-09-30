# doctors/models.py
from django.db import models
from users.models import User 

class Doctor(models.Model):
    # Primary key automatically added by Django as 'id' with AutoField
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        related_name='doctor_profile'
    )
    full_name = models.CharField(max_length=100, null=False)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.specialization})"
