# billing/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BillingRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    doctor_queue = models.ForeignKey('patients.DoctorQueue', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, default="Consultation Fee")
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.description} - {self.amount}"
