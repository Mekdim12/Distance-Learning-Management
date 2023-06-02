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
import random
import os
# Create your views here.

@login_required(login_url='base_login_page')
@school_teacher_only
def teacher_main_landing_page(request):
    return render(request,'Teacher/index.html' )



@login_required(login_url='base_login_page')
@school_teacher_only
def teacher_logout(request):
    logout(request)
    return redirect('site_main_landing_page')


@login_required(login_url='base_login_page')
@school_teacher_only
def manage_personal_account(request):
    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    if request.method == 'POST':
        first_name = request.POST['firstname'].strip()
        middle_name = request.POST['middlename'].strip()
        last_name = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        gender = request.POST['gender'].strip()
        phone_number = request.POST['phonenumber'].strip()
        address = request.POST['address'].strip()
        email = request.POST['email'].strip()
        old_password = request.POST['oldpassword'].strip()
        new_password = request.POST['newpassword'].strip()

        if first_name != "":
            current_employe_object.firstname = first_name
        if middle_name != "":
            current_employe_object.middlename = middle_name
        if last_name != "":
            current_employe_object.lastname = last_name

        if middle_name != "":
            current_employe_object.middlename = middle_name

        if gender != "":
            current_employe_object.gender = gender

        if phone_number != "":
            current_employe_object.phonenumber = phone_number

        if address != "":
            current_employe_object.address = address

        if email != "":
            current_employe_object.email = email

        if username != "":
            current_employe_object.username = username 
            user_object.username = username

        if old_password != "" and new_password != "":
            if old_password != new_password:
                user_object.set_password(new_password)

        try:
            current_employe_object.save()
            user_object.save()
            print("XXXXXXXXXXXXXXXX 90 UPDATED teacher  personal info XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('teacher_main_landing_page')
        except Exception as e:
            print(e)
            print("XXXXXXXXXXXXXXXX    91 FAIL teacher personal account inf update   XXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('teacher_main_landing_page')

    context = {
        'user_infn':user_object,
        'personal_info':current_employe_object
    }
    return render(request , 'Teacher/personal_account_mgt.html', context=context)


@login_required(login_url='base_login_page')
@school_teacher_only
def teacher_student_information_view_page(request):
    
    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    try:
        assigned_coureses_list = TeacherToCourseMapping.objects.filter(teacher = current_employe_object)
        list_coureses_realted = []
        for coureses in assigned_coureses_list:
            [list_coureses_realted.append(x)if x not in list_coureses_realted else None  for x in coureses.course_info.all()]

        lits_dep_teacher_is_teaching = []
        for coures in list_coureses_realted:
            coureses_list = Courseinformations.objects.filter(course_id = coures.course_id )
            for related in coureses_list:
                if related.departement not in lits_dep_teacher_is_teaching:
                    lits_dep_teacher_is_teaching.append(related.departement)
        list_student_related = []
        for dep in lits_dep_teacher_is_teaching:
            student_with_current_dep = StudentAcademicOption.objects.filter(departement = dep)
            [list_student_related.append(y) if y not in list_student_related else None for y in student_with_current_dep ]
        
        

        student_for_degree_program = StudentAcademicOption.objects.filter(programs = 'Bchelor Degree')
        student_for_masteres_program = StudentAcademicOption.objects.filter(programs = 'Masters Degree')

        dep_for_students = {}
        
        bsc_students = []
        for bsc in  student_for_degree_program:
            if bsc in list_student_related:
                bsc_students.append(bsc)
                student = StudentAcademicOption.objects.get(student_id = bsc.student_id)
                dep_for_students[bsc] = student.departement
                
        msc_students = []
        for msc in  student_for_masteres_program:
            if msc in list_student_related:
                msc_students.append(msc)
                student = StudentAcademicOption.objects.get(student_id = msc.student_id)
                dep_for_students[msc] = student.departement
       
        context = {
            'msc_student':msc_students,
            'bsc_students':bsc_students,
            'is_bsc_len':len(bsc_students),
            'is_msc_len':len(msc_students),
            'stud_map_with_dep': dep_for_students,
            'is_there_any_coures_assigned':len(assigned_coureses_list)
        }

    except Exception as e:
        return redirect('teacher_main_landing_page')
    

    try:
        return render(request, 'Teacher/student_information_mgt_page.html', context = context)
    except Exception as e:
        print(e)
        return redirect('teacher_main_landing_page')

@login_required(login_url='base_login_page')
@school_teacher_only
def student_detail_information_display_page(request, student_id):
    
    student_info = StudentInformation.objects.get(userid = student_id)
    
    context = {
        'student_info': student_info,
    }

    return render(request, 'Teacher/student_information_detail_view_page.html',context = context)