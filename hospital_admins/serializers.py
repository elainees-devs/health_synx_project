# hospital_admins/serializers.py
from rest_framework import serializers
from .models import HospitalAdminProfile
from users.models import User


class HospitalAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the HospitalAdminProfile model.
    Includes related user details for readability.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HospitalAdminProfile
        fields = [
            'id',
            'user',
            'user_details',
            'department',
        ]
        read_only_fields = []

    def get_user_details(self, obj):
        """Return minimal user info for convenience."""
        if obj.user:
            return {
                "id": obj.user.id,
                "username": obj.user.username,
                "email": obj.user.email,
                "user_role": obj.user.role,
            }
        return None

    def create(self, validated_data):
        """Ensure the user is assigned the correct role."""
        user = validated_data.get('user')
        if user and user.role != 'hospital_admin':
            user.role = 'hospital_admin'
            user.save()
        return super().create(validated_data)
