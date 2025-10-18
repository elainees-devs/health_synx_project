# appointments/forms.py
from django import forms
from .models import Appointment
from users.models import User

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show doctors in the dropdown
        self.fields['doctor'].queryset = User.objects.filter(role='doctor')
