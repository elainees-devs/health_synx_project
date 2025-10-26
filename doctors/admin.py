# doctors/admin.py
from django.contrib import admin
from .models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'specialization', 'license_number')
    search_fields = ('user__username', 'user__email', 'specialization', 'license_number')
    autocomplete_fields = ('user',)
