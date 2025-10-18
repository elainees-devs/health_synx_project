# nurse/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User
from users.decorators import role_required  

@login_required
@role_required(['nurse'])
def nurse_dashboard(request):
    """
    Display all registered patients with links to record vitals.
    """
    patients = User.objects.filter(role='patient').select_related('patientprofile')

    return render(request, 'users/dashboards/nurse_dashboard.html', {
        'patients': patients
    })

# -----------------------------
# List all patients (role='patient')
# -----------------------------
@login_required
@role_required(['nurse'])
def patient_list(request):
    patients = User.objects.filter(role='patient')
    context = {
        'patients': patients,
    }
    # Use the existing template from patients app
    return render(request, 'patients/patient_list.html', context)
