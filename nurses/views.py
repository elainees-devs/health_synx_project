# nurses/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import RolePermission
from users.models import User
from users.serializers import UserSerializer


class NursePatientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for nurses to view all patients.
    Only users with role='nurse' can access.
    """
    queryset = User.objects.filter(role='patient').select_related('patientprofile').order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, RolePermission] 
    allowed_roles = ['nurse']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset
