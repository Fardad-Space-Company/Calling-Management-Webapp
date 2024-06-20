from django.contrib import admin
from .models import EmployeeID

class EmployeeIDAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id']  # Specify fields to display in the admin list view

admin.site.register(EmployeeID, EmployeeIDAdmin)