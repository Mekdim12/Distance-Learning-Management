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
    path('TeacherManagement/view', views.doh_teacher_to_course_mapping_mgt_page, name='teacher_to_course_mgt_page' ),
    path('TeacherManagement/Insert', views.doh_teacher_to_course_mapping_insert_page, name='teacher_to_course_insert_page' ),
    path('TeacherManagement/Edit/<slug:teacher_id>', views.doh_teacher_to_course_mapping_editing_page, name='teacher_to_course_edit_page' ),
    path('CourseManagement/View', views.doh_course_management_page, name='doh_course_management' ),
    path('CourseManagement/Edit/<slug:course_info>', views.doh_course_information_edit, name='doh_course_info_edit' ),
    
    
]