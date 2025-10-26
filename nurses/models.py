# nurses/models.py
from django.db import models
from users.models import User
from departments.models import Department

class NurseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional nurse-specific info
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nurses'
    )
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)

    def clean(self):
        """Ensure the user has role 'nurse'."""
        if self.user.user_role != 'nurse':
            from django.core.exceptions import ValidationError
            raise ValidationError(f"User {self.user.email} is not a nurse.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.user_role})"
