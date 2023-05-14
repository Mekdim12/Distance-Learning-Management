from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.school_admin_landingpage, name="landing_page_school_admin"),
    path('Adminlogin',views.login_page, name="admin_login_page"),
    path('AdminlandingPage', views.admin_main_landing_page , name="admin_main_landing_page"),
    path('Adminlogout', views.school_admin_logout, name="school_admin_logout") , 
    path('AdminPersonalAccount',views.school_admin_personal_account, name="admin_personal_account"),
    path('AdminViewTeachers',views.admin_manage_teacher ,name="view_list_teachers"),
    path('AdminTeacherInformationInsert', views.admin_teacher_inserting_information, name="admin_teacher_information_insert"),
    path('AdminTeacherInformation/Delete/<slug:eployee_id>' , views.admin_teacher_information_deleting_url, name="teacher_info_delete"),
    path('AdminTeacherInformation/Edit/<slug:eployee_id>' , views.admin_teacher_information_editing_url, name="teacher_info_edit"),
    path('AdminViewRegisterar', views.admin_manage_registerar, name='view_list_registerar'),
    path('AdminRegisterar/Insert', views.admin_registerar_info_insert, name="admin_registerar_information_insert"),
    path('AdminRegisterar/Delete/<slug:eployee_id>', views.admin_registerar_delete, name="admin_delete_registerar"),
    path('AdminRegisterar/Edit/<slug:eployee_id>', views.admin_regiseterar_information_edit, name="admin_edit_registerar"),
    path('AdminView',views.admin_list_of_adminstrations_staffs, name="admin_staffs_display_page"), 
    path('AdminView/Insert',views.school_admin_registering_page, name="new_admin_info_inserting_page"),
    path('AdminView/Delete/<slug:eployee_id>',views.school_admin_account_delete, name="admin_info_deleting_page")
]
