# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Customize how the User model appears in Django Admin"""

    # Fields shown in the list view
    list_display = ('username', 'email', 'role', 'department', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'department')

    # Fields that link to the detail view
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Fieldsets for viewing/editing a user in the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'department', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for adding a new user in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'role',
                'department', 'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )


