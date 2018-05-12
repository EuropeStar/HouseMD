from rest_framework import viewsets, permissions
from .serializers import *
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core import helpers
from core.models import *


class DiseasesViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer


class SymptomViewSet(viewsets.ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer


class MedViewSet(viewsets.ModelViewSet):
    queryset = Med.objects.all()
    serializer_class = MedSerializer


class ContraindicationViewSet(viewsets.ModelViewSet):
    queryset = Contraindication.objects.all()
    serializer_class = SymptomSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ActiveSubstanceViewSet(viewsets.ModelViewSet):
    queryset = ActiveSubstance.objects.all()
    serializer_class = ActiveSubstanceSerializer


class SideEffectViewSet(viewsets.ModelViewSet):
    queryset = SideEffect.objects.all()
    serializer_class = SideEffectSerializer


class AnalysisParamsViewSet(viewsets.ModelViewSet):
    queryset = AnalysisParams.objects.all()
    serializer_class = AnalysisParamsSepializer


class ExaminationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(doctor=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

@api_view(['GET'])
def get_user_info(request):
    return Response(ProfileSerializer(data=request.user.profile).data)


@api_view(['GET'])
def main(request):
    user = request.user
    last_notifications = Notification.objects.filter(user=user).order_by('-date_time')[:2]
    last_examinatinos = Examination.objects.filter(doctor=user).order_by('-date_time')[:2]
    #notifications_amount = Notification.objects.filter(user=user).count()

    notifs_serializer = NotificationSerializer(last_notifications, many=True)
    notifs_data = notifs_serializer.data

    exams_serializer = ExaminationSerializer(last_examinatinos, many=True)
    exams_data = exams_serializer.data

    data = {
        'notifications': notifs_data,
        'examinations': exams_data
    }

    return Response(data)

@api_view(['GET', 'POST'])
def profile(request):
    if request.method == 'GET':
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        profile_data = serializer.data
        return Response(profile_data)
    elif request.method == 'POST':
        _type = request.data['type']
        if _type == 'private':
            if request.data['first_name'] and request.data['last_name']:
                request.user.first_name = request.data['first_name']
                request.user.last_name = request.data['last_name']
                request.user.save()
                return Response(status=200)
            else:
                return Response(status=400)


@api_view(['GET'])
def notifications(request):
    user = request.user
    notifs = Notification.objects.filter(user=user)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def save_examination(request, pk):
    helpers.calc_probability(pk=pk, doctor=request.user, patient=request.data["patient"],
                             sex=request.data["sex"], age=request.data["age"],
                             sym=request.data["symptoms"], analysis=request.data["analysis"])
    examination = Examination.objects.get(pk=pk)
    serializer = ExaminationSerializer(examination)
    return Response(serializer.data)
