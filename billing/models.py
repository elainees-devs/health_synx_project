# billing/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BillingRecord(models.Model):
    CATEGORY_CHOICES = [
        ('consultation', 'Consultation'),
        ('pharmacy', 'Pharmacy & Medicine'),
        ('lab', 'Laboratory'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'}
    )
    doctor_queue = models.ForeignKey(
        'patients.DoctorQueue', on_delete=models.CASCADE, null=True, blank=True
    )

    # Add category to distinguish billing types
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='consultation'
    )

    description = models.CharField(max_length=255, default="Consultation Fee")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.get_category_display()} - {self.amount}"
