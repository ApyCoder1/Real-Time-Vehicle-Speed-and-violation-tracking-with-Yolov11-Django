from rest_framework import serializers
from .models import SpeedRecord

class SpeedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedRecord
        fields = '__all__'
