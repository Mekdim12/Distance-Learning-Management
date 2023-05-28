
from django.contrib import admin
from django.urls import path, include
from . import views, views_fd

urlpatterns = [
    path('', views.registerars_landing_page, name="registerar_main_landing_page"),    
    path('PersonalAccount', views.manage_personal_account, name="registerar_presonal_account_mgt"),
    path('RegisterarLogout', views.registerar_logout, name="regisetrar_account_logout"),
    path('StudentManagement', views.student_information_management_page, name="registerar_student_info_mgt"),
    path('StudentManagement/Insert', views.student_information_inserting_page, name="registerar_student_info_insert"),
    path('StudentManagement/Edit/<slug:stud_id>', views.student_information_editing_page, name="registerar_student_info_edit"),
    path('StudentManagement/Delete/<slug:stud_id>', views.student_information_deleting_page, name="registerar_student_info_delete"),
    path('StudentManagement/TakePhoto/<slug:stud_id>',views.photo_taken_page, name="add_photos_page"),
    path('StudentManagement/TakingPhoto/<slug:studentid>',views_fd.add_photos, name="add_photos"),
    path('StudentManagement/TrainModelpage',views.registerar_train_model, name="train_model_page"),
    path('StudentManagement/TrainModel' ,views_fd.train, name="train_model"),
    path('StudentManagement/Duedate' ,views.registerar_duedate_page, name="due_date_management"),
    path('StudentManagement/payementManagement' ,views.student_management_payement_mgt, name="student_mgt_payment"),
]

