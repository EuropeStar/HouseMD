from django.urls import path

from core import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('main/', views.main, name='main'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
]
