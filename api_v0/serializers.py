from rest_framework.serializers import ModelSerializer
from core.models import *

class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'
