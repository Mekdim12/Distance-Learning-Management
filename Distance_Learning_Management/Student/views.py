from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import *
from School_Admin.models import *
from Reception.models import *
from Doh.models import *
from .models import *
from Teacher.forms import *
from Teacher.models import *
from django.contrib import messages
import random
import os

# Create your views here.


@login_required(login_url='base_login_page')
@school_student_only
def homepage_for_student(request):
    return render(request, "Student/index.html")

@login_required(login_url='base_login_page')
@school_student_only
def personal_account_management_std(request):
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)
    
    student_acadmaic_option = StudentAcademicOption.objects.get(student_id = current_std_object)
    
    context = {
        'student_info':current_std_object,
        'acadamic_info':student_acadmaic_option
    }
    return render(request, 'Student/personal_account_mgt.html', context=context)

@login_required(login_url='base_login_page')
@school_student_only
def student_logout(request):
    logout(request)
    return redirect('base_login_page')

@login_required(login_url='base_login_page')
@school_student_only
def student_course_list_view(request):
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)

    student_acadmaic_option = StudentAcademicOption.objects.get(student_id = current_std_object)
    
    course_list = Courseinformations.objects.filter(departement =student_acadmaic_option.departement,  programs =student_acadmaic_option.programs)

    context = {
        "acadamic_option":student_acadmaic_option,
        "program":student_acadmaic_option.programs,
        'courses':course_list,
        'is_course_empty':len(course_list) > 0
    }
    return render(request, 'Student/course_list_display_page.html', context = context)
    

@login_required(login_url='base_login_page')
@school_student_only
def list_of_courses_materials_for_specific_courses(request, course_id):
    selectedcourse = Courseinformations.objects.get(course_id = course_id)
    list_course_materials = MainCoursecontentdetailcontent.objects.filter(courseid = selectedcourse)
    context = {
        "course_id":course_id,
        "is_empty":len(list_course_materials) > 0,
        "course_materials":list_course_materials,
    }

    return render(request, 'Student/course_view_detail_list.html', context= context)


@login_required(login_url='base_login_page')
@school_student_only
def course_information_detail_view_page(request, course_id, course_detail_view):
    detailCourseInformation = MainCoursecontentdetailcontent.objects.get(id = course_detail_view)

    valusToPopulated = {
        "pdf":detailCourseInformation.pdf,
        "audio":detailCourseInformation.audio,
        "video":detailCourseInformation.video,
        "notes":detailCourseInformation.notes,
        "topic":detailCourseInformation.topic,
    }
    
    form = MainCoursecontentdetailcontentForm(valusToPopulated)
    
    context = {
        "course_id":course_id,
        "detailInfn"  :detailCourseInformation,
        "form":form
    }

    return render(request,'Student/course_content_display_page.html', context)

@login_required(login_url='base_login_page')
@school_student_only
def assignment_course_list_view_page(request):
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)

    student_acadmaic_option = StudentAcademicOption.objects.get(student_id = current_std_object)
    
    course_list = Courseinformations.objects.filter(departement =student_acadmaic_option.departement,  programs =student_acadmaic_option.programs)

    context = {
        "acadamic_option":student_acadmaic_option,
        "program":student_acadmaic_option.programs,
        'courses':course_list,
        'is_course_empty':len(course_list) > 0
    }
    return render(request, 'Student/assignment_course_list_page.html', context = context)

@login_required(login_url='base_login_page')
@school_student_only
def assignment_list_view_for_course_specific(request, course_id):
    course_information = Courseinformations.objects.get(course_id = course_id)
    list_of_assignment = AssignmentContent.objects.filter(courseinfn = course_information)
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)


    interaction = dict()
    for assignment in list_of_assignment:
        try:
            AssignmentStudentInteraction.objects.get(stduentid = current_std_object, assignment = assignment)
            interaction[assignment.id] = True
        except:
            interaction[assignment.id] = False

    context ={
        'list_of_interaction': interaction,
        'list_of_assignment':list_of_assignment,
        'is_assingment_empty':len(list_of_assignment) > 0,
        'course_id':course_id
    }
    return render(request, "Student/assignment_list_for_course_specific_page.html", context = context)


@login_required(login_url='base_login_page')
@school_student_only
def assignment_detail_student_view(request, course_id, assignment_id):

    
    assignement_content = AssignmentContent.objects.get(id = assignment_id)
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)
    
    if request.method == "POST":
        pdf = request.FILES['assignment']
        try:
            AssignmentStudentInteraction.objects.create(
                stduentid = current_std_object,
                assignment = assignement_content,
                is_submitted = True,
                submitted = pdf
            )
            print("xxxxxxxxxxxxxx 116 successfully submited assignments  xxxxxxxxxxxx")
            return redirect('assignment_list_view_for_course_specific', course_id)
        except:
            print("xxxxxxx 115 Failed to save student sunmitted assignement xxxxxxxxxxxxx")
    
    is_submiited = False
    try:
        inter = AssignmentStudentInteraction.objects.get(stduentid = current_std_object, assignment = assignement_content)
        if inter.is_submitted:
            is_submiited = True
        else:
            is_submiited = False
    except:
        is_submiited =False
    
    

    context = {
        "assingment":assignement_content,
        'course_id':course_id,
        'assignment_id':assignment_id,
        'is_submiited':is_submiited
    }

    try:
        mark = AssignmentAssesment.objects.get(stduentid = current_std_object, assignment_id = assignement_content  )
        if is_submiited:
            context['evaluation'] = mark
            context['isevaluated'] = True
    except:
        if is_submiited:
             context['isevaluated'] = False

    return render(request, "Student/assignment_detail_view_page.html", context = context)



