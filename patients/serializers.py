# patients/serializers.py
from rest_framework import serializers
from users.models import User
from .models import (
    PatientProfile,
    PatientVitals,
    DoctorQueue,
    DoctorNote,
    PrescriptionItem,
    Prescription,
)
from pharmacy.models import Medicine


# -----------------------------
# Serializer for Patient Model
# -----------------------------
class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    dob = serializers.DateField(source='patientprofile.dob', required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'dob', 'is_active', 'date_joined',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        profile_data = validated_data.pop('patientprofile', {})
        validated_data.pop('role', None)  # Remove role to avoid duplicates

        username = validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f"User '{username}' already exists.")

        # Create user with explicit role
        user = User.objects.create_user(**validated_data, role='patient')

        # Only create PatientProfile if it doesn't exist
        PatientProfile.objects.get_or_create(user=user, defaults=profile_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('patientprofile', {})

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create PatientProfile
        profile, created = PatientProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance




# -----------------------------
# Serializer for Patient Vitals
# -----------------------------
class PatientVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVitals
        fields = [
            'id',
            'temperature',
            'pulse_rate',
            'recorded_at',
        ]
        read_only_fields = ['recorded_at']


# -----------------------------
# Serializer for Doctor Queue
# -----------------------------
class DoctorQueueSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    vitals = PatientVitalsSerializer(read_only=True)

    class Meta:
        model = DoctorQueue
        fields = [
            'id',
            'patient',
            'vitals',
            'doctor',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# -----------------------------
# Serializer for Doctor Note
# -----------------------------
class DoctorNoteSerializer(serializers.ModelSerializer):
    # SerializerMethodFields are read-only and automatically call get_<field>
    doctor = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    queue_info = serializers.SerializerMethodField()

    # Input fields for POST
    patient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='patient'),
        write_only=True
    )
    queue_item = serializers.PrimaryKeyRelatedField(
        queryset=DoctorQueue.objects.all(),
        write_only=True
    )

    class Meta:
        model = DoctorNote
        fields = [
            'id',
            'doctor',
            'patient',
            'patient_name',
            'queue_item',
            'queue_info',
            'diagnosis',
            'prescription',
            'created_at',
        ]
        read_only_fields = ['doctor', 'patient_name', 'queue_info', 'created_at']

    # SerializerMethodField methods
    def get_doctor(self, obj):
        if obj.doctor:
            return f"{obj.doctor.first_name} {obj.doctor.last_name}"
        return None

    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None

    def get_queue_info(self, obj):
        if obj.queue_item:
            return {
                "id": obj.queue_item.id,
                "status": obj.queue_item.status,
                "patient": f"{obj.queue_item.patient.first_name} {obj.queue_item.patient.last_name}",
                "created_at": obj.queue_item.created_at,
            }
        return None

    # Attach logged-in doctor automatically
    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user
        return super().create(validated_data)


# -----------------------------
# Serializer for Prescription Item
# -----------------------------
class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Medicine.objects.all()
    )

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medicine', 'dosage']


# -----------------------------
# Serializer for Prescription
# -----------------------------
class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='doctor'))
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='patient'))
    items = PrescriptionItemSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['id', 'doctor', 'patient', 'queue_item', 'date_issued', 'status', 'notes', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        prescription = Prescription.objects.create(**validated_data)
        for item_data in items_data:
            PrescriptionItem.objects.create(prescription=prescription, **item_data)
        return prescription
