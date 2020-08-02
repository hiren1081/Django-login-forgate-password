from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('forgate/', views.forgate, name='forgate'),
    path('recover/', views.recover, name='recover'),
    
]