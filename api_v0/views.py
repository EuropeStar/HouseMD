from rest_framework import viewsets

from .serializers import *


# Create your views here.

# @api_view(['GET'])
# def api_root(request, format=None):
#     """
#     The entry endpoint of our API.
#     """
#     return Response({
#         'users': reverse('user-list', request=request),
#         'groups': reverse('group-list', request=request),
#     })

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

class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# class UserList(generics.ListCreateAPIView):
#     model = User
#     serializer_class = UserSerializer
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     model = User
#     serializer_class = UserSerializer
#
#
# class DiseasesList(generics.ListCreateAPIView):
#     model = Disease
#     serializer_class = DiseaseSerializer
#
# class DiseasesDetail(generics.RetrieveUpdateDestroyAPIView):
#     model = Disease
#     serializer_class = DiseaseSerializer
