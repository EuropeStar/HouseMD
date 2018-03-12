from django.shortcuts import render
from rest_framework import viewsets
from core.models import *
from .serializers import DiseaseSerializer
# Create your views here.

class DiseasesViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer