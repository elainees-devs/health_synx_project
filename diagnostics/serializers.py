# diagnostics/serializers.py
from rest_framework import serializers
from .models import LabTest, LabQueue, XRay, XRayQueue, MRI, MRIQueue
from users.models import User


# -----------------------------
# LAB SERIALIZERS
# -----------------------------
class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['id', 'name', 'description', 'normal_range', 'created_at']


class LabQueueSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    technician_name = serializers.CharField(source='technician.get_full_name', read_only=True)
    lab_test_detail = LabTestSerializer(source='lab_test', read_only=True)

    class Meta:
        model = LabQueue
        fields = [
            'id', 'patient', 'patient_name', 'lab_test', 'lab_test_detail',
            'technician', 'technician_name', 'status', 'results', 'created_at'
        ]


# -----------------------------
# XRAY SERIALIZERS
# -----------------------------
class XRaySerializer(serializers.ModelSerializer):
    class Meta:
        model = XRay
        fields = ['id', 'name', 'description', 'created_at']


class XRayQueueSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    technician_name = serializers.CharField(source='technician.get_full_name', read_only=True)
    xray_detail = XRaySerializer(source='xray', read_only=True)

    class Meta:
        model = XRayQueue
        fields = [
            'id', 'patient', 'patient_name', 'xray', 'xray_detail',
            'technician', 'technician_name', 'status', 'results', 'created_at'
        ]


# -----------------------------
# MRI SERIALIZERS
# -----------------------------
class MRISerializer(serializers.ModelSerializer):
    class Meta:
        model = MRI
        fields = ['id', 'name', 'description', 'created_at']


class MRIQueueSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    technician_name = serializers.CharField(source='technician.get_full_name', read_only=True)
    mri_detail = MRISerializer(source='mri', read_only=True)

    class Meta:
        model = MRIQueue
        fields = [
            'id', 'patient', 'patient_name', 'mri', 'mri_detail',
            'technician', 'technician_name', 'status', 'results', 'created_at'
        ]
