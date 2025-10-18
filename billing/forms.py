# billing/forms.py
from django import forms

from .models import BillingRecord
from patients.models import DoctorQueue

class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = ['patient', 'doctor_queue', 'amount', 'description', 'paid']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor_queue': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor_queue'].queryset = DoctorQueue.objects.filter(status='completed')