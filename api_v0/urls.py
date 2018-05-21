from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import *

router = DefaultRouter()

# register urls here

router.register(r'diseases', DiseasesViewSet)
router.register(r'symptoms', SymptomViewSet)
router.register(r'meds', MedViewSet)
router.register(r'contraindications', ContraindicationViewSet)
router.register(r'active_substances', ActiveSubstanceViewSet)
router.register(r'side_effects', SideEffectViewSet)
router.register(r'analysis_params', AnalysisParamsViewSet)
router.register(r'examinations', ExaminationViewSet)
router.register(r'notifications', NotificationViewSet)


urlpatterns = [
    url('^', include(router.urls)),
    url('^api_auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api_obtain_token', obtain_jwt_token),
    url(r'api_refresh_token', refresh_jwt_token),
    url(r'get_user_info', get_user_info),
    path('dashboard', main, name='main'),
    path('profile', profile, name='profile'),
    path('notifications', notifications, name='notifications'),
    path('save-examination', save_examination, name='save-examination'),
    path('save-examination/<int:pk>', save_examination, name='save-examination'),
    path('research_meta', request_research_meta, name='research_meta')
]
