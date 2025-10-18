# doctors/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from .models import DoctorProfile

class DoctorRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50, required=False)
    surname = forms.CharField(max_length=50)
    id_number = forms.CharField(max_length=20)
    specialization = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=10)
    email = forms.EmailField()
    license_number = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
