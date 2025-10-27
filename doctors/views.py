# doctors/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import User
from patients.models import DoctorQueue, DoctorNote, Prescription, PrescriptionItem
from pharmacy.models import Medicine
from billing.models import BillingRecord
from .serializers import DoctorProfileSerializer
from patients.serializers import (
    DoctorQueueSerializer,
    DoctorNoteSerializer,
    PrescriptionItemSerializer,
    PrescriptionSerializer
)
from users.permissions import RolePermission
from core.pagination import StandardResultsSetPagination


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list all doctors (read-only).
    Accessible by: admin, nurse, doctor
    """
    from doctors.models import DoctorProfile
    queryset = DoctorProfile.objects.select_related('user').all().order_by('user__first_name')
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    pagination_class = StandardResultsSetPagination


class DoctorQueueViewSet(viewsets.ModelViewSet):
    """
    Manage doctor queues — used by doctors to manage patient flow.
    """
    queryset = DoctorQueue.objects.all().select_related('patient', 'doctor').order_by('-created_at')
    serializer_class = DoctorQueueSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['get'])
    def waiting(self, request):
        """
        List all patients currently waiting to see a doctor.
        """
        queue = self.queryset.filter(status='waiting')
        serializer = self.get_serializer(queue, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update queue status:
        with_doctor | sent_to_lab | sent_to_pharmacy | completed
        """
        queue_item = self.get_object()
        new_status = request.data.get('status')

        valid_status = ['with_doctor', 'sent_to_lab', 'sent_to_pharmacy', 'completed']
        if new_status not in valid_status:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        queue_item.status = new_status
        queue_item.doctor = request.user
        queue_item.save()

        return Response({
            "message": f"Queue status updated to '{new_status}' for patient {queue_item.patient.username}."
        }, status=status.HTTP_200_OK)


class DoctorNoteViewSet(viewsets.ModelViewSet):
    """
    Allows doctors to record notes for patients.
    """
    queryset = DoctorNote.objects.all().select_related('patient', 'doctor', 'queue_item')
    serializer_class = DoctorNoteSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        """
        Automatically attach the logged-in doctor to the note.
        """
        # FIX: Use doctor's profile (if needed), ensure test expects correct doctor format
        serializer.save(doctor=self.request.user)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    Allows doctors to create and manage prescriptions for patients.
    """
    queryset = Prescription.objects.all().select_related('patient', 'doctor')
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'])
    def add_items(self, request, pk=None):
        """
        Add prescription items (medicine + dosage) to a prescription.
        Automatically updates patient queue status to 'sent_to_pharmacy'.
        """
        prescription = self.get_object()
        medicine_ids = request.data.get('medicine_id', [])
        dosages = request.data.get('dosage', [])

        if not isinstance(medicine_ids, list):
            medicine_ids = [medicine_ids]
        if not isinstance(dosages, list):
            dosages = [dosages]

        if not medicine_ids or not dosages:
            return Response(
                {"error": "Both 'medicine_id' and 'dosage' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(medicine_ids) != len(dosages):
            return Response(
                {"error": "Each medicine must have a matching dosage."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_items = []
        for med_id, dosage in zip(medicine_ids, dosages):
            medicine = get_object_or_404(Medicine, id=med_id)
            item = PrescriptionItem.objects.create(
                prescription=prescription,
                medicine=medicine,
                dosage=dosage
            )
            created_items.append(PrescriptionItemSerializer(item).data)

        # Update the doctor's queue status for this patient
        DoctorQueue.objects.filter(
            patient=prescription.patient,
            status__in=['with_doctor', 'waiting']
        ).update(status='sent_to_pharmacy')

        return Response({
            "message": "Prescription items added and patient sent to pharmacy.",
            "items": created_items
        }, status=status.HTTP_201_CREATED)
