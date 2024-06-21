from django.contrib import admin
from django.urls import path
from .views import  custom_login, custom_logout, profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)