# patients/models.py
from django.db import models

from users.models import User
from doctors.models import DoctorProfile
from billing.models import BillingRecord

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    assigned_doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        # Get user's full name
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()

class PatientVitals(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    temperature = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 37.2°C
    pulse_rate = models.PositiveIntegerField()  # beats per minute
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.patient.get_full_name()} at {self.recorded_at}"
    
class DoctorQueue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('with_doctor', 'With Doctor'),
        ('sent_to_lab', 'Sent to Lab'),
        ('sent_to_pharmacy', 'Sent to Pharmacy'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'patient'},
        related_name='queue_as_patient'  # <--- new
    )
    vitals = models.ForeignKey('PatientVitals', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'doctor'},
        related_name='queue_as_doctor'  # <--- new
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self):
        self.status = 'completed'
        self.save()
        # Create a billing record with description
        BillingRecord.objects.create(
            patient=self.patient,
            doctor_queue=self,
            amount=self.calculate_charges(),
            description="Consultation Fee"  # you can make this dynamic later
        )

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.status}"
    

class DoctorNote(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='doctor_notes_as_patient' 
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'},
        related_name='doctor_notes_as_doctor' 
    )
    queue_item = models.ForeignKey(DoctorQueue, on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

