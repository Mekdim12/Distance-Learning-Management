
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.registerars_landing_page, name="registerar_main_landing_page"),    
    path('PersonalAccount', views.manage_personal_account, name="registerar_presonal_account_mgt"),
    path('RegisterarLogout', views.registerar_logout, name="regisetrar_account_logout"),
    path('StudentManagement', views.student_information_management_page, name="registerar_student_info_mgt"),
    path('StudentManagement/Insert', views.student_information_inserting_page, name="registerar_student_info_insert"),
    path('StudentManagement/Edit/<slug:stud_id>', views.student_information_editing_page, name="registerar_student_info_edit"),
    path('StudentManagement/Delete/<slug:stud_id>', views.student_information_deleting_page, name="registerar_student_info_delete"),
]

