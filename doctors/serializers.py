# doctors/serializers.py
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer
from .models import DoctorProfile



class DoctorProfileSerializer(serializers.ModelSerializer):
    """Main serializer for DoctorProfile."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialization', 'license_number']

    def get_fields(self):
        """
        Override get_fields() to allow filtering user list in admin or write mode.
        """
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            fields['user'] = serializers.PrimaryKeyRelatedField(
                queryset=User.objects.filter(role='doctor')
            )
        return fields

    def validate_user(self, value):
        """
        Ensure only users with role='doctor' can be linked.
        """
        if value.role != 'doctor':
            raise serializers.ValidationError("The linked user must have the role 'doctor'.")
        return value
