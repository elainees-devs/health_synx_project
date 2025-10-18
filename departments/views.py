# departments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Department
from .forms import DepartmentForm
from users.decorators import role_required

@login_required
@role_required(['admin', 'hospital_admin'])
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
@role_required(['admin','hospital_admin'])
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/add_department.html', {'form': form})

@login_required
@role_required(['admin', 'hospital_admin'])
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/edit_department.html', {'form': form})

@login_required
@role_required(['admin', 'hospital_admin'])
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, f'Department "{department.name}" has been deleted.')
        return redirect('department_list')
    return render(request, 'departments/delete_department.html', {'department': department})
