# hospital_admins/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import HospitalAdmin
from .serializers import HospitalAdminSerializer
from users.permissions import IsAdminUser  
from core.pagination import StandardResultsSetPagination


class HospitalAdminViewSet(viewsets.ModelViewSet):
    """
    REST API endpoints for managing Hospital Admins.
    Only users with admin privileges can create, update, or delete hospital admins.
    """
    queryset = HospitalAdmin.objects.all().order_by('-created_at')
    serializer_class = HospitalAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Hospital Admin registered successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Hospital Admin updated successfully.", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": f"Hospital Admin '{instance.user.username}' deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
