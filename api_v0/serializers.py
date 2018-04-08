from rest_framework.serializers import ModelSerializer

from core.models import *


class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class SymptomSerializer(ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class MedSerializer(ModelSerializer):
    class Meta:
        model = Med
        fields = '__all__'


class ContraindicationSerializer(ModelSerializer):
    class Meta:
        model = Contraindication
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ActiveSubstanceSerializer(ModelSerializer):
    class Meta:
        model = ActiveSubstance
        fields = '__all__'


class SideEffectSerializer(ModelSerializer):
    class Meta:
        model = SideEffect
        fields = '__all__'

class ExaminationSerializer(ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'