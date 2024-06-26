from django.urls import path
from . import views 
from django.contrib import admin


urlpatterns = [
    path('', views.management, name='management'),
    path('fetch_postcodes/', views.fetch_postcodes, name='fetch_postcodes'),
    path('table-list/', views.table_list, name='table_list'),
    path('shop/',views.chooseshop, name='shopchoosing' ),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('shop/data_entry/<int:shop_id>/', views.data_entry, name='data_entry'),
    path('shop/crmbackend', views.crmbackend_data, name='crmbackend'),
    path('call-history', views.call_history, name='call-history'),
    path('error/', views.errorhandling, name= 'error_url' ),
    path('get-username/<int:employeeID>/',views.get_username_by_employee_id, name='get_username_by_employee_id')
    
]