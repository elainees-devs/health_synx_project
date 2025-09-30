# prescriptions/models.py
from django.db import models
from records.models import MedicalRecord

class Prescription(models.Model):
    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    medicine_name = models.CharField(max_length=100, null=False)
    dosage = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.medicine_name} for record {self.record.id}"
