
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.registerars_landing_page, name="registerar_main_landing_page"),    
    path('PersonalAccount', views.manage_personal_account, name="registerar_presonal_account_mgt"),
    path('RegisterarLogout', views.registerar_logout, name="regisetrar_account_logout")
]

