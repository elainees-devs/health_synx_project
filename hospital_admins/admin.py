# hospital_admins/admin.py
from django.contrib import admin
from .models import HospitalAdminProfile

@admin.register(HospitalAdminProfile)
class HospitalAdminProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department')
    list_filter = ('department',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ()
    ordering = ('id',)
