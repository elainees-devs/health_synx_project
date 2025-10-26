# patients/models.py
from django.db import models
from django.conf import settings
from users.models import User


# ---------------------------------------------------------------------
# Patient profile linked to a User account
# ---------------------------------------------------------------------
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    assigned_doctor = models.ForeignKey(
        'doctors.DoctorProfile',  # use string reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or self.user.username


# ---------------------------------------------------------------------
# Model to record vital signs for a patient
# ---------------------------------------------------------------------
class PatientVitals(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )
    temperature = models.DecimalField(max_digits=4, decimal_places=1)  # e.g., 37.2°C
    pulse_rate = models.PositiveIntegerField()  # beats per minute
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.patient.get_full_name()} at {self.recorded_at}"


# ---------------------------------------------------------------------
# Queue model to track patient status during consultation
# ---------------------------------------------------------------------
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
        related_name='queue_as_patient'
    )
    vitals = models.ForeignKey('PatientVitals', on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'doctor'},
        related_name='queue_as_doctor'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self):
        """Mark consultation as completed and create a billing record."""
        self.status = 'completed'
        self.save()
        from billing.models import BillingRecord  # avoid circular import
        BillingRecord.objects.create(
            patient=self.patient,
            doctor_queue=self,
            amount=self.calculate_charges(),
            description="Consultation Fee"
        )

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.status}"


# ---------------------------------------------------------------------
# Doctor's notes and diagnosis for a patient visit
# ---------------------------------------------------------------------
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

    def __str__(self):
        return f"Doctor Note by {self.doctor.get_full_name()} for {self.patient.get_full_name()}"


# ---------------------------------------------------------------------
# Prescription model linked to a patient and doctor
# ---------------------------------------------------------------------
class Prescription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispensed', 'Dispensed'),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='prescriptions_as_patient'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_prescriptions',
        limit_choices_to={'role': 'doctor'}
    )
    date_issued = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    queue_item = models.ForeignKey(DoctorQueue, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.patient.username} by {self.doctor.username if self.doctor else 'Unknown'}"


# ---------------------------------------------------------------------
# Prescription items model linking medicines to prescriptions
# ---------------------------------------------------------------------
class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items'
    )
    medicine = models.ForeignKey('pharmacy.Medicine', on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)  # e.g., "1 tablet twice a day"

    def __str__(self):
        return f"{self.medicine.name} for {self.prescription.patient.username}"
