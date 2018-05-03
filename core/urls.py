from django.conf.urls import url
from django.urls import path, include

from core.views import *

app_name = 'core'
urlpatterns = [
    path('db/', insert_connections),
    path('sign-in/', sign_in, name='sign-in'),
    path('api_obtain_token/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('main/', main, name='main'),
    path('profile/', profile, name='profile'),
    path('notifications/', notifications, name='notifications'),
    path('save-examination/<int:pk>', save_examination, name='save-examination'),
  
    # api urls

    url(r'^api/v0/', include('api_v0.urls'))
]
