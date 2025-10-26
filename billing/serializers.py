# billing/serializers.py
from rest_framework import serializers
from .models import BillingRecord


from rest_framework import serializers
from .models import BillingRecord

class BillingRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for BillingRecord model
    Used in BillingRecordViewSet for CRUD and custom endpoints.
    """

    # Return full patient name
    patient_name = serializers.SerializerMethodField()
    patient_id = serializers.IntegerField(source='patient.id', read_only=True)

    class Meta:
        model = BillingRecord
        fields = [
            'id',
            'patient',        # original foreign key (optional if you want)
            'patient_name',   # full name
            'patient_id',     # id for reference
            'category',
            'description',
            'amount',
            'paid',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_patient_name(self, obj):
        """Return 'First Last' format"""
        if obj.patient.first_name or obj.patient.last_name:
            return f"{obj.patient.first_name} {obj.patient.last_name}".strip()
        return obj.patient.username  # fallback
