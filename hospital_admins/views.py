# hospital_admins/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HospitalAdminRegistrationForm

def register_hospital_admin(request):
    if request.method == 'POST':
        form = HospitalAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hospital Admin registered successfully.")
            return redirect('hospital_admin_list')
    else:
        form = HospitalAdminRegistrationForm()
    return render(request, 'hospital_admins/register_hospital_admin.html', {'form': form})
