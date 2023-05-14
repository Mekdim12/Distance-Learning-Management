from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.school_admin_landingpage, name="landing_page_school_admin"),
    path('Adminlogin',views.login_page, name="admin_login_page"),
    path('AdminlandingPage', views.admin_main_landing_page , name="admin_main_landing_page"),
    path('Adminlogout', views.school_admin_logout, name="school_admin_logout") , 
    path('AdminPersonalAccount',views.school_admin_personal_account, name="admin_personal_account"),
    path('AdminViewTeachers',views.admin_manage_teacher ,name="view_list_teachers"),
    path('AdminTeacherInformationInsert', views.admin_teacher_inserting_information, name="admin_teacher_information_insert")
]
