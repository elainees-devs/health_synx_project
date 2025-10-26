# departments/admin.py
from django.contrib import admin
from .models import Department, DepartmentStaff


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model"""
    list_display = ('name', 'description')
    search_fields = ('name',)  # Required for autocomplete support
    ordering = ('name',)


@admin.register(DepartmentStaff)
class DepartmentStaffAdmin(admin.ModelAdmin):
    """Admin configuration for DepartmentStaff model"""
    list_display = ('department', 'get_staff_name', 'get_staff_role')
    list_filter = ('department', 'staff__role')
    autocomplete_fields = ('department', 'staff')
    search_fields = (
        'department__name',
        'staff__username',
        'staff__first_name',
        'staff__last_name',
        'staff__email',
    )
    ordering = ('department__name',)

    def get_staff_name(self, obj):
        return obj.staff.get_full_name() or obj.staff.username
    get_staff_name.short_description = 'Staff Name'

    def get_staff_role(self, obj):
        return obj.staff.role
    get_staff_role.short_description = 'Role'
