from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken import views
router = DefaultRouter()

# register urls here

router.register(r'diseases', DiseasesViewSet)

urlpatterns = [
    url('^', include(router.urls)),
    url('^api_auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth$', views.obtain_auth_token, name='auth'),
]