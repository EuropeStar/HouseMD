from django.conf.urls import url
from django.urls import path, include

from core import views

app_name = 'core'
urlpatterns = [
    path('db/', views.insert_connections),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('personal_administration/', views.personal_administration, name='personal_administration'),
    path('history/', views.history, name='history'),
    path('confirmation/<int:examination_id>/', views.confirmation, name='confirmation'),
    # path('main/', views.main, name='main'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    # api urls
    url(r'^api/v0/', include('api_v0.urls'))
]
