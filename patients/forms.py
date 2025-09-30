# patients/forms.py
from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'full_name', 'date_of_birth', 'gender', 'contact', 'medical_history']
