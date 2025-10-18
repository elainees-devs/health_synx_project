# appointments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import Appointment
from .forms import AppointmentForm
from users.decorators import role_required

# -----------------------------
# Patient books an appointment
# -----------------------------
@login_required
@role_required(['patient'])
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # assign current patient
            appointment.save()
            return redirect('appointment_list')  # redirect to patient appointments
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book_appointment.html', {'form': form})

# ---------------------------------
# Patient views their appointments
# ---------------------------------
@login_required
@role_required(['patient'])
def patient_appointments(request):
    appointments = request.user.appointments.all()  # related_name in model
    return render(request, 'appointments/patient_appointments.html', {'appointments': appointments})

# -------------------------------
# Doctor views their appointments
# -------------------------------
@login_required
@role_required(['doctor'])
def doctor_appointments(request):
    appointments = request.user.doctor_appointments.all()  # related_name in model
    return render(request, 'appointments/doctor_appointments.html', {'appointments': appointments})

# -------------------------------
# Optional: Admin / staff view all appointments
# -------------------------------
@login_required
@role_required(['admin', 'hospital_admin'])
def all_appointments(request):
    appointments = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'appointments/all_appointments.html', {'appointments': appointments})
