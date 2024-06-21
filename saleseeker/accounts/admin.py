from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rule', 'email', 'image']
    search_fields = ['user__username', 'rule', 'email']

admin.site.register(Profile, ProfileAdmin)