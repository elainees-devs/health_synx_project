# billing/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBillingOrAdmin(BasePermission):
    """
    Custom permission to allow access only to users with 'billing' or 'admin' roles.
    Supports both read and write operations.
    """

    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user or not user.is_authenticated:
            return False

        # Allow safe methods (GET, HEAD, OPTIONS) for authenticated users
        if request.method in SAFE_METHODS:
            return True

        # Allow only admin or billing roles for modification
        return getattr(user, "role", None) in ["admin", "billing"]

    def has_object_permission(self, request, view, obj):
        """
        Optional fine-grained permission (object-level).
        Example: Billing officers can only modify unpaid bills.
        """
        user = request.user

        # Admins can access everything
        if getattr(user, "role", None) == "admin":
            return True

        # Billing officers can modify only unpaid bills
        if getattr(user, "role", None) == "billing":
            if request.method in SAFE_METHODS:
                return True
            return not getattr(obj, "paid", False)

        return False
