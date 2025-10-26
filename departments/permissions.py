from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrHospitalAdmin(BasePermission):
    """
    Allow read access to any authenticated user.
    Allow modifications only for admin or hospital_admin.
    """

    def has_permission(self, request, view):
        # Must be logged in
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow safe (read-only) methods for everyone authenticated
        if request.method in SAFE_METHODS:
            return True

        # Only allow write (POST, PUT, DELETE) for admin/hospital_admin
        return getattr(request.user, "role", None) in ["admin", "hospital_admin"]
