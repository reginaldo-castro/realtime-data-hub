from rest_framework import serializers
from .models import DataJob

class DataJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataJob
        fields = ['id', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']