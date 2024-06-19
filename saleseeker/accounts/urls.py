from django.contrib import admin
from django.urls import path
from .views import  custom_login, custom_logout, profile

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
 ]