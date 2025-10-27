# patients/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import User
from users.permissions import RolePermission
from .models import PatientProfile, PatientVitals, DoctorQueue
from .serializers import PatientSerializer, PatientVitalsSerializer, DoctorQueueSerializer
from billing.utils import create_consultation_fee
from core.pagination import StandardResultsSetPagination


class PatientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='patient').prefetch_related('patientprofile')
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    allowed_roles = ['admin', 'hospital_admin', 'nurse', 'doctor']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        # fallback for standard actions
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save()

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, RolePermission],
        serializer_class=PatientVitalsSerializer  # <-- This fixes Swagger
    )
    def record_vitals(self, request, pk=None):
        patient = self.get_object()
        serializer = self.get_serializer(data=request.data)  # uses serializer_class above
        serializer.is_valid(raise_exception=True)
        vitals = serializer.save(patient=patient)
        DoctorQueue.objects.create(patient=patient, vitals=vitals, status='waiting')
        return Response({"message": "Vitals recorded and patient added to queue."}, status=status.HTTP_201_CREATED)
       

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, RolePermission])
    def vitals(self, request, pk=None):
        """
        Get all vitals of a patient
        """
        patient = self.get_object()
        vitals = PatientVitals.objects.filter(patient=patient).order_by('-recorded_at')
        serializer = PatientVitalsSerializer(vitals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, RolePermission])
    def add_to_queue(self, request, pk=None):
        """
        Add patient to doctor queue based on latest vitals
        """
        patient = self.get_object()
        latest_vital = PatientVitals.objects.filter(patient=patient).order_by('-recorded_at').first()
        if not latest_vital:
            return Response({"error": "No vitals recorded yet."}, status=status.HTTP_400_BAD_REQUEST)
        if DoctorQueue.objects.filter(patient=patient, status__in=['waiting', 'with_doctor']).exists():
            return Response({"info": "Patient already in queue."}, status=status.HTTP_200_OK)

        DoctorQueue.objects.create(patient=patient, vitals=latest_vital, status='waiting')
        return Response({"message": "Patient added to doctor queue."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, RolePermission])
    def send_to_pharmacy(self, request, pk=None):
        """
        Send patient to pharmacy and create consultation billing
        """
        queue = get_object_or_404(DoctorQueue, id=pk)
        if queue.status != 'with_doctor':
            return Response({"error": "Patient must be with doctor before sending to pharmacy."},
                            status=status.HTTP_400_BAD_REQUEST)

        queue.status = 'sent_to_pharmacy'
        queue.save()

        create_consultation_fee(queue.patient, queue)
        return Response({"message": "Patient sent to pharmacy. Consultation fee added."}, status=status.HTTP_200_OK)
