from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from core import helpers
from rest_framework import viewsets


from core import helpers
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


class AnalysisParamsViewSet(viewsets.ModelViewSet):
    queryset = AnalysisParams.objects.all()
    serializer_class = AnalysisParamsSepializer

class ExaminationViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    
     def retrieve(self, request, pk=None, *args, **kwargs):
        helpers.calc_probability(pk=pk, doctor=request.user, patient="")
        queryset = Examination.objects.all()
        ex = get_object_or_404(queryset, pk=pk)
        serializer = ExaminationSerializer(ex)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

