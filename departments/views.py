# departments/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Department
from .serializers import DepartmentSerializer
from .permissions import IsAdminOrHospitalAdmin  

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    REST API endpoints for managing departments.
    Only users with 'admin' or 'hospital_admin' roles can modify departments.
    """
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHospitalAdmin] 

    def get_queryset(self):
        """
        Optionally filter or customize the department listing.
        """
        return Department.objects.all().order_by('name')

    def create(self, request, *args, **kwargs):
        """
        Create a new department (admin/hospital_admin only)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Department created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing department
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Department updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a department (admin/hospital_admin only)
        """
        instance = self.get_object()
        name = instance.name
        instance.delete()
        return Response(
            {"message": f"Department '{name}' deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
