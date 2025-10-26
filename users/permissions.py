# users/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

class RolePermission(BasePermission):
    """
    Custom permission that handles both authentication (401)
    and role authorization (403).
    """

    def has_permission(self, request, view):
        # --- Handle unauthenticated users (401) ---
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("Authentication credentials were not provided.")

        # --- Role-based access (403 if not allowed) ---
        allowed_roles = getattr(view, "allowed_roles", None)
        user_role = getattr(request.user, "role", None)

        # Admins/superusers always have access
        if request.user.is_superuser:
            return True

        # If allowed_roles not set → allow all authenticated users
        if not allowed_roles:
            return True

        if user_role not in allowed_roles:
            raise PermissionDenied("You do not have permission to perform this action.")

        return True
