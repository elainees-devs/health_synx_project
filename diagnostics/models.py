# diagnostics/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# -----------------------------
# LAB TEST MODELS
# -----------------------------
class LabTest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    normal_range = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['id', 'name']



class LabQueue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_queues')
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='lab_technician')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    results = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_test.name} for {self.patient.get_full_name()}"
    
    class Meta:
        ordering = ['id', 'created_at']


# -----------------------------
# XRAY MODELS
# -----------------------------
class XRay(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id', 'name']



class XRayQueue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xray_queues')
    xray = models.ForeignKey(XRay, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='xray_technician')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    results = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.xray.name} for {self.patient.get_full_name()}"
    
    class Meta:
        ordering = ['id', 'created_at']


# -----------------------------
# MRI MODELS
# -----------------------------
class MRI(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id', 'name']


class MRIQueue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mri_queues')
    mri = models.ForeignKey(MRI, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='mri_technician')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    results = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mri.name} for {self.patient.get_full_name()}"
    
    class Meta:
        ordering = ['id', 'created_at']
