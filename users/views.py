# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum


from .decorators import role_required
from .forms import UserRegisterForm, UserLoginForm
from departments.models import Department
from .models import User
from patients.forms import PatientForm
from patients.models import DoctorQueue
from billing.models import BillingRecord

def register_user(request):
    form = UserRegisterForm(request.POST or None)
    departments = Department.objects.all()  # Fetch all departments

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        dept_id = request.POST.get("department")
        if dept_id:
            user.department_id = dept_id
        user.save()
        messages.success(request, f"Account {user.username} created successfully!")
        return redirect("login")

    return render(request, "register.html", {"form": form, "departments": departments})

@csrf_protect
def custom_login(request):
    form = UserLoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Try authenticate with username
            user = authenticate(request, username=username_or_email, password=password)

            # Try authenticate with email
            if user is None:
                from users.models import User
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                return redirect("redirect_after_login")
            else:
                form.add_error(None, "Incorrect username/email or password.")  # Non-field error

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)  # Ends the session
    return redirect('login')  # Redirect to login page or homepage

# Redirect users after login based on role
@login_required
def redirect_after_login(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')

    role_redirects = {
        'doctor': 'doctor_dashboard',
        'patient': 'patient_dashboard',
        'pharmacist': 'pharmacist_dashboard',
        'lab_tech': 'lab_tech_dashboard',
        'imaging_tech': 'imaging_tech_dashboard',
        'billing': 'billing_dashboard',
        'nurse': 'nurse_dashboard',
        'hospital_admin': 'hospital_admin_dashboard',
    }

    return redirect(role_redirects.get(user.role, 'login'))



# Doctor dashboard
@login_required
@role_required(['doctor'])
def doctor_dashboard(request):
    # Get all patients currently waiting or with doctor
    queue = DoctorQueue.objects.filter(status__in=['waiting', 'with_doctor']).order_by('created_at')

    # Count total patients
    total_patients = queue.count()

    return render(request, 'users/dashboards/doctor_dashboard.html', {
        'queue': queue,
        'total_patients': total_patients
    })

# Hospital Admin dashboard
@login_required
@role_required(['hospital_admin'])
def hospital_admin_dashboard(request):
    return render(request, 'users/dashboards/hospital_admin_dashboard.html')


# Nurse dashboard
@login_required
@role_required(['nurse'])
def nurse_dashboard(request):
    return render(request, 'users/dashboards/nurse_dashboard.html')

# Billing Officer dashboard
@login_required
@role_required(['admin', 'billing'])
def billing_dashboard(request):
    # Get total counts and sums
    total_bills = BillingRecord.objects.count()
    total_pending = BillingRecord.objects.filter(paid=False).count()
    total_collected = BillingRecord.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get recent 5 bills
    recent_bills = BillingRecord.objects.order_by('-created_at')[:5]

    context = {
        'total_bills': total_bills,
        'total_pending': total_pending,
        'total_collected': total_collected,
        'recent_bills': recent_bills,
    }

    return render(request, 'users/dashboards/billing_dashboard.html', context)

# Admin dashboard
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


