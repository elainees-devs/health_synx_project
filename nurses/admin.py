# nurse/admin.py
from django.contrib import admin
from .models import NurseProfile

@admin.register(NurseProfile)
class NurseProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_full_name', 'get_email', 'department', 'specialization', 'license_number')
    search_fields = ('user__username', 'user__email', 'department__name', 'specialization', 'license_number')  # required for autocomplete
    autocomplete_fields = ('user', 'department')
    list_filter = ('department',)
    ordering = ('user__username',)

    # Display user full name
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

    # Display user email
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
