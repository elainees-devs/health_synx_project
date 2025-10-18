# doctors/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from users.decorators import role_required
from users.models import User
from patients.models import DoctorQueue, DoctorNote
from patients.forms import DoctorNoteForm
from billing.models import BillingRecord

# -----------------------------
# List all doctors
# -----------------------------
@login_required
@role_required(['superuser', 'admin', 'nurse', 'doctor'])
def doctor_list(request):
    # Assuming doctors have role='doctor'
    doctors = User.objects.filter(role='doctor')
    
    context = {
        'doctors': doctors,
    }
    return render(request, 'doctors/doctor_list.html', context)

@login_required
@role_required(['doctor'])
def doctor_queue(request):
    queue = DoctorQueue.objects.filter(status='waiting').order_by('created_at')
    return render(request, 'doctors/doctor_queue.html', {'queue': queue})


@login_required
@role_required(['doctor'])
def update_queue_status(request, queue_id, action):
    queue_item = get_object_or_404(DoctorQueue, id=queue_id)
    
    if action in ['with_doctor', 'sent_to_lab', 'sent_to_pharmacy', 'completed']:
        queue_item.status = action
        queue_item.doctor = request.user
        queue_item.save()
    
    return redirect('doctor_queue')

@login_required
@role_required(['doctor'])
def see_patient(request, queue_id):
    queue_item = get_object_or_404(DoctorQueue, id=queue_id)

    if request.method == 'POST':
        form = DoctorNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.patient = queue_item.patient
            note.doctor = request.user
            note.queue_item = queue_item
            note.save()

            # Check if doctor clicked 'Completed'
            if 'completed' in request.POST:
                queue_item.status = 'completed'
                queue_item.save()

                # Create billing record
                billing = BillingRecord.objects.create(
                    patient=queue_item.patient,
                    doctor_queue=queue_item,
                    amount=1200.00,  # default fee
                    description="Consultation Fee",
                    paid=False
                )
                print("Billing record created:", billing)
            else:
                queue_item.status = 'with_doctor'
                queue_item.save()

            return redirect('doctor_queue')
    else:
        form = DoctorNoteForm()

    return render(request, 'doctors/see_patient.html', {
        'queue_item': queue_item,
        'form': form
    })



@login_required
@role_required(['doctor'])
def doctor_dashboard(request):
    """
    Display the doctor dashboard with the current patient queue.
    """
    # Get all patients currently waiting or with doctor
    queue = DoctorQueue.objects.filter(status__in=['waiting', 'with_doctor']).order_by('created_at')

    # Optional: count total patients in queue
    total_patients = queue.count()

    return render(request, 'doctors/doctor_dashboard.html', {
        'queue': queue,
        'total_patients': total_patients
    })