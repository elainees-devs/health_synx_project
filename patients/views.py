# patients/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.utils.text import slugify  
import uuid

from users.models import User
from .models import PatientProfile, PatientVitals, DoctorQueue
from .forms import PatientForm, PatientVitalsForm
from users.decorators import role_required 


User = get_user_model()


# ---------------------------------------------------------------------
# List all patients
# ---------------------------------------------------------------------
@login_required
@role_required(['admin', 'hospital_admin', 'nurse', 'doctor'])
def patient_list(request):
    patients = User.objects.filter(role='patient').select_related('patientprofile')
    return render(request, 'patients/patient_list.html', {'patients': patients})

# ---------------------------------------------------------------------
# Add a new patient
# ---------------------------------------------------------------------
@login_required
@role_required(['admin', 'hospital_admin'])
def add_patient(request):
    form = PatientForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            patient = form.save(commit=False)

            # Generate unique username
            first_name = patient.first_name.strip() if patient.first_name else ''
            last_name = patient.last_name.strip() if patient.last_name else ''
            email = patient.email.strip() if patient.email else ''
            base_username = slugify(f"{first_name}-{last_name}") or "patient"
            username = base_username

            while User.objects.filter(username=username).exists():
                username = f"{base_username}-{get_random_string(4)}"

            # Create user safely
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password="defaultpassword123",
                role='patient',
                gender=patient.gender,
                patient_type=patient.patient_type,
                phone_number=patient.phone_number,
            )

            # Link patient profile
            patient.user = user
            patient.save()

            messages.success(request, f"Patient '{first_name} {last_name}' added successfully!")
            return redirect('patient_list')
        else:
            messages.error(request, "Please correct the errors below.")

    # Always render the form on GET or invalid POST
    return render(request, 'patients/add_patient.html', {'form': form})

# ---------------------------------------------------------------------
# Edit existing patient details
# ---------------------------------------------------------------------
@login_required
@role_required(['admin', 'hospital_admin'])
def edit_patient(request, pk):
    user = get_object_or_404(User, pk=pk, role='patient')
    profile, created = PatientProfile.objects.get_or_create(user=user)

    # Pre-fill dob value in form
    initial_data = {'dob': profile.dob}
    form = PatientForm(request.POST or None, instance=user, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            profile.dob = form.cleaned_data.get('dob')
            profile.save()
            messages.success(request, 'Patient details updated successfully!')
            return redirect('patient_list')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'patients/edit_patient.html', {'form': form, 'patient': user})

# ---------------------------------------------------------------------
# Delete patient
# ---------------------------------------------------------------------
@login_required
@role_required(['admin', 'hospital_admin'])
def delete_patient(request, pk):
    patient = get_object_or_404(User, pk=pk, role='patient')
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient_list')
    return render(request, 'patients/delete_patient.html', {'patient': patient})

@login_required
@role_required(['admin', 'nurse'])
def record_vitals(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='patient')

    if request.method == 'POST':
        form = PatientVitalsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.patient = patient
            vitals.save()

            #  Add patient to doctor's queue
            DoctorQueue.objects.create(
                patient=patient,
                vitals=vitals,
                status='waiting'
            )
            return redirect('patient_list')
    else:
        form = PatientVitalsForm()

    return render(request, 'patients/record_vitals.html', {'form': form, 'patient': 
    patient})

@login_required
@role_required(['nurse'])
def patient_vitals(request, patient_id):
    """
    Display all recorded vitals for a single patient.
    """
    patient = get_object_or_404(User, id=patient_id, role='patient')
    vitals = PatientVitals.objects.filter(patient=patient).order_by('-recorded_at')  # newest first

    return render(request, 'patient_vitals.html', {
        'patient': patient,
        'vitals': vitals
    })

@login_required
@role_required(['nurse'])
def all_patients_vitals(request):
    """
    Display all patients along with their recorded vitals.
    """
    patients = User.objects.filter(role='patient').prefetch_related('patientvitals_set')

    # Optional: Build a dict of patient -> vitals if needed in template
    patient_vitals = {patient: patient.patientvitals_set.all().order_by('-recorded_at') for patient in patients}

    return render(request, 'patients/all_patients_vitals.html', {
        'patient_vitals': patient_vitals
    })

@login_required
def doctor_dashboard(request):
    # Get all users with role 'patient'
    patients = User.objects.filter(role='patient').prefetch_related('vitals')

    # Get each patient's latest vital
    patient_data = []
    for patient in patients:
        latest_vital = patient.vitals.order_by('-recorded_at').first()
        patient_data.append({
            'patient': patient,
            'latest_vital': latest_vital
        })

    return render(request, 'users/doctor_dashboard.html', {'patient_data': patient_data})

@login_required
@role_required(['nurse'])
def add_patient_to_queue(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='patient')
    
    # Get latest vitals
    latest_vital = PatientVitals.objects.filter(patient=patient).order_by('-recorded_at').first()
    if not latest_vital:
        messages.error(request, f"Cannot add {patient.get_full_name()} to queue: no vitals recorded yet.")
        return redirect('all_patients_vitals')

    # Use patient_id to avoid object identity issues
    if DoctorQueue.objects.filter(patient_id=patient.id, status__in=['waiting', 'with_doctor']).exists():
        messages.info(request, f"{patient.get_full_name()} is already in the doctor queue.")
        return redirect('all_patients_vitals')

    # Add patient to doctor queue
    DoctorQueue.objects.create(
        patient=patient,
        vitals=latest_vital,
        status='waiting'
    )
    messages.success(request, f"{patient.get_full_name()} added to the doctor's queue.")
    return redirect('all_patients_vitals')
