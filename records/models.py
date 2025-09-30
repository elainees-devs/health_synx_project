# records/models.py
from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone

class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medical_records'
    )
    diagnosis = models.TextField(null=False)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Record for {self.patient.full_name} on {self.date}"
