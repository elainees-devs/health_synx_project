# nurses/serializers.py
from rest_framework import serializers
from users.models import User
from .models import NurseProfile

# Serializer for nested user info
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'date_joined', 'is_active')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# Serializer for nurses to view patient info
class PatientForNurseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'date_joined',
            'is_active',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# Serializer for NurseProfile (read-only nested user)
class NurseProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = NurseProfile
        fields = ('id', 'user', 'department', 'phone_number', 'specialization', 'license_number')


# Serializer for creating/updating NurseProfile
class NurseProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseProfile
        fields = ('user', 'department', 'phone_number', 'specialization', 'license_number')
