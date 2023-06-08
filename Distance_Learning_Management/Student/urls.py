from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from ckeditor_uploader import views as ckeditor_views

from django.contrib.auth.decorators import *
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path('', views.homepage_for_student, name='student_main_landing_page' ),
]