# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    role = forms.ChoiceField(choices=User.ROLES)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'date_of_birth', 'role', 'password1', 'password2']