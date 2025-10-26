# diagnostics/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import LabTest, LabQueue, XRay, XRayQueue, MRI, MRIQueue
from .serializers import (
    LabTestSerializer, LabQueueSerializer,
    XRaySerializer, XRayQueueSerializer,
    MRISerializer, MRIQueueSerializer
)
from users.permissions import RolePermission
from diagnostics.utils import create_diagnostic_fee  


# -----------------------------
# LAB VIEWSETS
# -----------------------------
class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all().order_by('name')
    serializer_class = LabTestSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class LabQueueViewSet(viewsets.ModelViewSet):
    queryset = LabQueue.objects.select_related('patient', 'lab_test', 'technician').order_by('-created_at')
    serializer_class = LabQueueSerializer
    permission_classes = [IsAuthenticated, RolePermission]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark lab test as completed, save results, and create billing"""
        queue_item = self.get_object()
        results = request.data.get('results')
        if not results:
            return Response({"error": "Results are required"}, status=status.HTTP_400_BAD_REQUEST)

        queue_item.status = 'completed'
        queue_item.results = results
        queue_item.save()

        # Add lab fee to billing
        create_diagnostic_fee(queue_item.patient, queue_item, test_type='lab')

        serializer = self.get_serializer(queue_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -----------------------------
# XRAY VIEWSETS
# -----------------------------
class XRayViewSet(viewsets.ModelViewSet):
    queryset = XRay.objects.all().order_by('name')
    serializer_class = XRaySerializer
    permission_classes = [IsAuthenticated, RolePermission]


class XRayQueueViewSet(viewsets.ModelViewSet):
    queryset = XRayQueue.objects.select_related('patient', 'xray', 'technician').order_by('-created_at')
    serializer_class = XRayQueueSerializer
    permission_classes = [IsAuthenticated, RolePermission]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark XRay test as completed, save results, and create billing"""
        queue_item = self.get_object()
        results = request.data.get('results')
        if not results:
            return Response({"error": "Results are required"}, status=status.HTTP_400_BAD_REQUEST)

        queue_item.status = 'completed'
        queue_item.results = results
        queue_item.save()

        # Add XRay fee to billing
        create_diagnostic_fee(queue_item.patient, queue_item, test_type='xray')

        serializer = self.get_serializer(queue_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -----------------------------
# MRI VIEWSETS
# -----------------------------
class MRIViewSet(viewsets.ModelViewSet):
    queryset = MRI.objects.all().order_by('name')
    serializer_class = MRISerializer
    permission_classes = [IsAuthenticated, RolePermission]


class MRIQueueViewSet(viewsets.ModelViewSet):
    queryset = MRIQueue.objects.select_related('patient', 'mri', 'technician').order_by('-created_at')
    serializer_class = MRIQueueSerializer
    permission_classes = [IsAuthenticated, RolePermission]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark MRI test as completed, save results, and create billing"""
        queue_item = self.get_object()
        results = request.data.get('results')
        if not results:
            return Response({"error": "Results are required"}, status=status.HTTP_400_BAD_REQUEST)

        queue_item.status = 'completed'
        queue_item.results = results
        queue_item.save()

        # Add MRI fee to billing
        create_diagnostic_fee(queue_item.patient, queue_item, test_type='mri')

        serializer = self.get_serializer(queue_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
