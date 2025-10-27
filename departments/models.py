# departments/models.py
from django.db import models

from users.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']  # Order departments by ID

    
    
class DepartmentStaff(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
        'role__in': ['doctor', 'lab_tech', 'imaging_tech', 'pharmacist', 'nurse', 'hospital_admin']
    })

    def __str__(self):
        return f"{self.staff.get_full_name()} ({self.department.name})"
    
    class Meta:
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['staff']),
        ]
        ordering = ['id']  # Order staff assignments by ID
