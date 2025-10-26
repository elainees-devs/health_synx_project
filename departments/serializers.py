# departments/serializers.py
from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department model.
    """
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']
