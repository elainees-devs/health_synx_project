# departments/admin.py
from django.contrib import admin
from .models import Department, DepartmentStaff

admin.site.register(Department)
admin.site.register(DepartmentStaff)
