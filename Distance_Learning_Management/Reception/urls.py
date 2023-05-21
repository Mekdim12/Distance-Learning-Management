
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.registerars_landing_page, name="registerar_main_landing_page"),    
]

