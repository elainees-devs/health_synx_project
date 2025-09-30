# prescriptions/forms.py
from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['record', 'medicine_name', 'dosage', 'duration']
        widgets = {
            'record': forms.Select(attrs={'class': 'form-control'}),
            'medicine_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medicine Name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosage'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration'}),
        }
