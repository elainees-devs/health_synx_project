# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect

from .decorators import role_required
from .forms import UserRegisterForm, UserLoginForm
from departments.models import Department
from users.models import User

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
# Redirect users after login based on role
@login_required
def redirect_after_login(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')
    elif user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    elif user.role == 'pharmacist':
        return redirect('pharmacist_dashboard')
    elif user.role == 'lab_tech':
        return redirect('lab_tech_dashboard')
    elif user.role == 'imaging_tech':
        return redirect('imaging_tech_dashboard')
    elif user.role == 'billing':
        return redirect('billing_dashboard')
    elif user.role == 'nurse':
        return redirect('nurse_dashboard')
    elif user.role == 'hospital_admin':
        return redirect('hospital_admin_dashboard')
    else:
        return redirect('login')


# Doctor dashboard
@login_required
@role_required(['doctor'])
def doctor_dashboard(request):
    return render(request, 'users/dashboards/doctor_dashboard.html')

# Hospital Admin dashboard
@login_required
@role_required(['hospital_admin'])
def hospital_admin_dashboard(request):
    return render(request, 'users/dashboards/hospital_admin_dashboard.html')




# Admin dashboard
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


