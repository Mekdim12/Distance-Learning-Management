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
    path('PersonalAccount', views.manage_personal_account, name="teacher_personal_account"),
    path('StudentInformation', views.teacher_student_information_view_page, name="student_information_mgt_page_by_teacher"),
    path('StudentInformation/Detail/<slug:student_id>', views.student_detail_information_display_page, name="student_information_detail_page_by_teacher"),
    path('CourseInformation/CourseSpecific', views.manage_course_information_teacher, name="course_information_mgt_by_teacher"),
    path('CourseInformation/CourseSpecific/ListView/<slug:course_id>', views.course_specific_management_page, name="specific_course_information_mgt_by_teacher"),
    path('CourseInformation/CourseSpecific/Insert/<slug:course_id>', views.course_specific_main_content_inserting_page, name="course_specific_main_content_inserting_page"),
    path('CourseInformation/CourseSpecific/PreviewUpdate/<slug:course_id>/<slug:content_id>', views.course_specific_main_content_preview_and_update_page, name="course_specific_main_content_preview_update_page"),
    path('ExamInformation/CourseList', views.teacher_examination_mgt_course_view_page, name="teacher_examination_mgt_course_view_page"),
    path('ExamInformation/ExamList/<slug:course_id>',views.exam_management_for_course_specific, name="exam_management_for_course_specific"),
    path('ExamInformation/Insert/<slug:course_id>',views.exam_management_question_and_answer_inserting_page, name="exam_mgt_question_and_answer_inserting_page"),
    path('ExamInformation/DetailView/<slug:course_id>/<slug:examsection_id>',views.exam_management_detail_view_page, name='exam_management_detail_view_page'),
    path('AssignmentInformation/CourseList',views.assignment_mgt_course_list_view_page, name='assignment_mgt_course_list_view_page'),
    path('AssignmentInformation/CourseSpecific/<slug:course_id>',views.assignment_mgt_course_specific_list_view_page, name='assignment_mgt_course_specific_list_view_page'),
    path('AssignmentInformation/Uploading/<slug:course_id>', views.assignment_mgt_assignment_uploding_page, name="assignment_mgt_assignment_uploding_page"),
    path('AssignmentInformation/DetailView/<slug:course_id>/<slug:assignment_id>', views.assignment_content_detail_view_page, name="assignment_content_detail_view_page")

]