from django.conf.urls import url
from django.urls import path, include

from core.views import *

app_name = 'core'
urlpatterns = [
    path('db/', views.insert_connections),
    path('sign-in/', sign_in, name='sign-in'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('main/', main, name='main'),
    path('profile/', profile, name='profile'),
    path('notifications/', notifications, name='notifications'),
  
    # api urls
    url(r'^api/v0/', include('api_v0.urls'))
]
