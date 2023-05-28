from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from ckeditor_uploader import views as ckeditor_views

from django.contrib.auth.decorators import *
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path('', views.departement_head_page, name='doh_main_landing_page' ),
    path('PersonalAccount/Edit', views.manage_personal_account, name='doh_personal_account_edit_page' ),
    path('Logout', views.doh_account_logout, name='doh_acc_logout' ),
    
]