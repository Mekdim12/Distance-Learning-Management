from django.urls import path
from django.conf import settings

from django.contrib.auth.decorators import *

from . import views

urlpatterns = [
    path('', views.homepage_for_student, name='student_main_landing_page' ),
    path('personaAccount', views.personal_account_management_std, name="student_personal_acoount_mgt"),
    path('Studentlogout',views.student_logout, name="studentlogout"),
    path('CourseList', views.student_course_list_view, name="student_course_list_view"),
    path('Course/content/<slug:course_id>', views.list_of_courses_materials_for_specific_courses, name="list_of_courses_materials_for_specific_courses"),
    path('Course/View/<slug:course_id>/<slug:course_detail_view>', views.course_information_detail_view_page, name="course_detail_view_page"),
    path('Assignement/Courselist',views.assignment_course_list_view_page, name="assignment_course_list_view_page"),
    path('Assignement/list/<slug:course_id>',views.assignment_list_view_for_course_specific, name="assignment_list_view_for_course_specific"),
    path('Assignement/view/<slug:course_id>/<slug:assignment_id>',views.assignment_detail_student_view, name="assignment_detail_student_view"),

]
