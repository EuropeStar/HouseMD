from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

# register urls here

router.register(r'diseases', DiseasesViewSet)
router.register(r'symptoms', SymptomViewSet)
router.register(r'meds', MedViewSet)
router.register(r'contraindications', ContraindicationViewSet)
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'active_substances', ActiveSubstanceViewSet)
router.register(r'side_effects', SideEffectViewSet)
# router.register(r'examinations', ExaminationViewSet)
router.register(r'analysis_params', AnalysisParamsViewSet)
router.register(r'examinations', ExaminationViewSet)


urlpatterns = [
    url('^', include(router.urls)),
    url('^api_auth', include('rest_framework.urls', namespace='rest_framework')),
]