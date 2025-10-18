# patients/forms.py 
from django import forms

from users.models import User
from .models import PatientProfile, PatientVitals, DoctorNote

class PatientForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True,
        label='Date of Birth'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'patient_type',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'patient_type': forms.Select(attrs={'class': 'form-select'}),
        }

        labels = {
            'patient_type': 'Patient Type',
        }

    def save(self, commit=True):
        """
        Save User first, then create/update the related PatientProfile.
        """
        user = super().save(commit=False)
        user.role = 'patient'
        user.is_active = True

        if commit:
            user.save()
            # Save or create PatientProfile
            dob = self.cleaned_data.get('dob')
            profile, created = PatientProfile.objects.get_or_create(user=user)
            profile.dob = dob
            profile.save()
        return user
    
class PatientVitalsForm(forms.ModelForm):
    class Meta:
        model = PatientVitals
        fields = ['temperature', 'pulse_rate']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pulse_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DoctorNoteForm(forms.ModelForm):
    class Meta:
        model = DoctorNote
        fields = ['diagnosis', 'prescription']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
        }
