# patients/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from .forms import PatientForm 
from django.contrib.auth.decorators import login_required

# ---------------------------------------------------------
# List all patients
# ---------------------------------------------------------
@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

# ---------------------------------------------------------
# View a single patient's details
# ---------------------------------------------------------
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patients/patient_detail.html', {'patient': patient})

# ---------------------------------------------------------
# Create a new patient
# ---------------------------------------------------------
@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})

# ---------------------------------------------------------
# Update an existing patient
# ---------------------------------------------------------
@login_required
def patient_update(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form})

# ---------------------------------------------------------
# Delete a patient
# ---------------------------------------------------------
@login_required
def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
