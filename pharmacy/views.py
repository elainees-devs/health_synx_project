# pharmacy/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Medicine, Supplier, StockTransaction
from patients.models import Prescription
from patients.serializers import PrescriptionSerializer
from .serializers import MedicineSerializer, SupplierSerializer
from users.permissions import RolePermission 
from billing.utils import create_pharmacy_fee
from core.pagination import StandardResultsSetPagination


# -----------------------------
# Medicine API
# -----------------------------
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all().order_by('name')
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated, RolePermission]  # pharmacist only
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'])
    def dispense(self, request, pk=None):
        """
        Dispense a medicine to a patient prescription.
        Expects 'prescription_id' in request.data
        """
        medicine = self.get_object()
        prescription_id = request.data.get('prescription_id')
        prescription = get_object_or_404(Prescription, id=prescription_id)

        if prescription.status == 'dispensed':
            return Response({'detail': 'Already dispensed.'}, status=status.HTTP_400_BAD_REQUEST)

        if medicine.stock < 1:
            return Response({'detail': 'Not enough stock.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct stock and record transaction
        medicine.stock -= 1
        medicine.save()
        StockTransaction.objects.create(
            medicine=medicine,
            transaction_type='dispense',
            quantity=-1,
            performed_by=request.user,
            remarks=f'Dispensed to {prescription.patient.get_full_name()}'
        )

        # Update prescription
        prescription.status = 'dispensed'
        prescription.save()

        # Add billing
        create_pharmacy_fee(prescription.patient, prescription.queue_item, medicine.price)

        return Response({'detail': f'{medicine.name} dispensed successfully.'})


# -----------------------------
# Supplier API
# -----------------------------
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('name')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, RolePermission]  # pharmacist only
    pagination_class = StandardResultsSetPagination


# -----------------------------
# Prescription API (read-only)
# -----------------------------
class PrescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Prescription.objects.all().order_by('-id')
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, RolePermission]  # pharmacist only
    pagination_class = StandardResultsSetPagination
