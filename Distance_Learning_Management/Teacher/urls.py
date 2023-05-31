from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from ckeditor_uploader import views as ckeditor_views

from django.contrib.auth.decorators import *
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path('', views.teacher_main_landing_page, name='teacher_main_landing_page' ),
    path('Teacher_logout', views.teacher_logout, name="teacher_logout"),
    path('Personal Sccount', views.manage_personal_account, name="teacher_personal_account"),

    
]