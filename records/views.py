from django.shortcuts import render, get_object_or_404, redirect
from .models import MedicalRecord
from .forms import MedicalRecordForm

# List all medical records
def record_list(request):
    records = MedicalRecord.objects.all()
    return render(request, 'records/record_list.html', {'records': records})

# View a single medical record
def record_detail(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'records/record_detail.html', {'record': record})

# Create a new medical record
def record_create(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'records/record_form.html', {'form': form, 'form_title': 'Add Medical Record', 'submit_button': 'Save'})

# Update an existing medical record
def record_update(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'records/record_form.html', {'form': form, 'form_title': 'Edit Medical Record', 'submit_button': 'Update'})

# Delete a medical record
def record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(request, 'records/record_confirm_delete.html', {'record': record})
