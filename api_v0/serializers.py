from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import *


class SymptomSerializer(ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class MedSerializer(ModelSerializer):
    class Meta:
        model = Med
        fields = '__all__'


class DiseaseSerializer(ModelSerializer):
    symptoms = SymptomSerializer(many=True)
    meds = MedSerializer(many=True)

    class Meta:
        model = Disease
        fields = '__all__'


class ContraindicationSerializer(ModelSerializer):
    class Meta:
        model = Contraindication
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "last_name", "first_name",)


class ProfileSerializer(ModelSerializer):
    # user_id = serializers.CharField(source='user.id')
    username = serializers.CharField(source='user.username')
    last_name = serializers.CharField(source='user.last_name')
    first_name = serializers.CharField(source='user.first_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Profile
        fields = ("id", "organisation", "specialization", "is_chief", "email", "first_name",
                  "last_name", "username",)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.user.email = attrs.get('user.email', instance.user.email)
            instance.user.first_name = attrs.get('user.first_name', instance.user.first_name)
            instance.user.last_name = attrs.get('user.last_name', instance.user.last_name)
            instance.user.username = attrs.get('user.username', instance.user.username)
            # instance.user.id = attrs.get('user.id', instance.user.id)
            return instance

        user = User.objects.create_user(id=attrs.get('user.id'))
        return Profile(user=user)

class ActiveSubstanceSerializer(ModelSerializer):
    class Meta:
        model = ActiveSubstance
        fields = '__all__'


class SideEffectSerializer(ModelSerializer):
    class Meta:
        model = SideEffect
        fields = '__all__'


class AnalysisParamsSepializer(ModelSerializer):
    class Meta:
        model = AnalysisParams
        fields = '__all__'


class DiseaseProbabilitySerializer(ModelSerializer):
    disease = DiseaseSerializer(many=False)

    class Meta:
        model = DiseaseProbability
        fields = '__all__'


class ExaminationSerializer(ModelSerializer):
    symptoms = SymptomSerializer(many=True)
    diseases = DiseaseProbabilitySerializer(many=True)
    analysis = AnalysisParamsSepializer(many=True)
    doctor = UserSerializer(many=False)

    class Meta:
        model = Examination
        fields = '__all__'

class NotificationSerializer(ModelSerializer):
    diagnosis = DiseaseSerializer(many=True)
    class Meta:
        model = Notification
        fields = '__all__'


class AnalysisConstantSerializer(ModelSerializer):
    class Meta:
        model = AnalysisConstants
        fields = '__all__'