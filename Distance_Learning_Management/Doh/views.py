from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import *
from School_Admin.models import *
from .models import *
import random
import os
# Create your views here.


@login_required(login_url='base_login_page')
@shoold_doh_only
def departement_head_page(request):
    return render(request, 'Doh/main_landing_page.html')


@login_required(login_url='base_login_page')
@shoold_doh_only
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
            print("XXXXXXXXXXXXXXXX 70 UPDATED DOh personal info XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('doh_main_landing_page')
        except Exception as e:
            print(e)
            print("XXXXXXXXXXXXXXXX    71 FAIL DOH personal account inf update   XXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('doh_main_landing_page')



    context = {
        'user_infn':user_object,
        'personal_info':current_employe_object
    }
    return render(request , 'Doh/personal_account_mgt.html', context=context)

@login_required(login_url='base_login_page')
@shoold_doh_only
def doh_account_logout(request):
    logout(request)
    return redirect('site_main_landing_page')

@login_required(login_url='base_login_page')
@shoold_doh_only
def doh_teacher_to_course_mapping_mgt_page(request):

    grouped_final = {}
    teachers = []


    for teacher_teach in TeacherToCourseMapping.objects.all():        
        if not grouped_final.keys().__contains__(teacher_teach.teacher.employeeid):
            teachers.append(teacher_teach.teacher)

    for init in teachers:
        grouped_final[init] = []

    
    for teacher_teach in TeacherToCourseMapping.objects.all(): 
        values = grouped_final[teacher_teach.teacher]
        values.append(teacher_teach.course_info.all())

        
    context = {
        'grouped': grouped_final,
        'is_empty': len(grouped_final),
    }

    
    return render(request , 'Doh/teacher_to_course_mgt_page.html', context)

@login_required(login_url='base_login_page')
@shoold_doh_only
def doh_teacher_to_course_mapping_insert_page(request):

    if request.method == 'POST':
        teacher = request.POST.getlist('teacher')[0]
        courses = request.POST.getlist('course')

        try:
            employee = Employee.objects.get(employeeid = teacher)

            
            teacher_to_course = TeacherToCourseMapping.objects.create(
                    teacher = employee,
            )
            for course in courses:
                course_ = Courseinformations.objects.get(course_id = course)
                
                teacher_to_course.course_info.add(course_)
                print("xxxxxxxxx 76 doh successfully insereted teacher to course information xxxxxxxxxxxxxxxx")
                return redirect('teacher_to_course_mgt_page')
        except Exception as e:
            print(e)
            print("xxxxxxxxxxxxxxxxx 77 doh failed to inserted teacher to course info xxxxxxxxxxxxxxxxxxx")


    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)
    dep = Department.objects.get(departement_head = current_employe_object)

    courses = Courseinformations.objects.filter(departement = dep)
    teachers = RoleInSchool.objects.filter(employee_role = 'Teacher')
    
    context = {
        'courses':courses,
        'teachers':teachers,
        'is_both_not_empty':len(courses) > 0 and len(teachers) > 0,
    }

    return render(request , 'Doh/teacher_to_course_Inserting.html', context = context)


@login_required(login_url='base_login_page')
@shoold_doh_only
def doh_teacher_to_course_mapping_editing_page(request, teacher_id):

    if request.method == 'POST':
        courses = request.POST.getlist('course')

        try:
            employee = Employee.objects.get(employeeid = teacher_id)

            
            teacher_to_course = TeacherToCourseMapping.objects.get(
                    teacher = employee,
            )
            teacher_to_course.delete()


            teacher_to_course = TeacherToCourseMapping.objects.create(
                    teacher = employee,
            )
            for course in courses:
                course_ = Courseinformations.objects.get(course_id = course)
                
                teacher_to_course.course_info.add(course_)



            print("xxxxxxxxx 78 doh successfully update teacher to course information xxxxxxxxxxxxxxxx")
            return redirect('teacher_to_course_mgt_page')
        except Exception as e:
            print(e)
            print("xxxxxxxxxxxxxxxxx 79 doh failed to Update teacher to course info xxxxxxxxxxxxxxxxxxx")
        


    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)
    dep = Department.objects.get(departement_head = current_employe_object)



    courses = Courseinformations.objects.filter(departement = dep)
    teacher = Employee.objects.get(employeeid = teacher_id)

    course_this_teachers_assigned = TeacherToCourseMapping.objects.filter(teacher = teacher)

    course_this_teachers_assigned_ = []

    for crs in course_this_teachers_assigned:
        for map in crs.course_info.all():
            course_this_teachers_assigned_.append(map)
    
    final_list_courses = []

    for course in courses:
        for mapped in course_this_teachers_assigned:
            for map in mapped.course_info.all():
            
                if course.course_id == map.course_id:
                    if [course, True] not in  final_list_courses and [course, False] not in  final_list_courses:
                        final_list_courses.append([course, True])
                


    for cours in courses:
        if ([cours, True] not in final_list_courses  ):
            final_list_courses.append([cours, False])



    context = {
        'course_this_teachers_assigned':course_this_teachers_assigned_,
        'courses':courses,
        'teacher':teacher,
        'final_list_courses':final_list_courses,
        'is_both_not_empty':len(courses) > 0 
    }
    

    return render(request , 'Doh/teacher_to_course_editing.html', context)


@login_required(login_url='base_login_page')
@shoold_doh_only
def doh_course_management_page(request):

    course_info = Courseinformations.objects.all()
    context = {
        'course_infos':course_info,
        'is_empty':len(course_info)
    }
    return render(request, 'Doh/course_management_page.html',context = context)

@login_required(login_url='base_login_page')
@shoold_doh_only
def doh_course_information_edit(request, course_info):

    if request.method == 'POST':
        course_name = request.POST['course_name'].strip()
        level_of_difficulties = request.POST['level_of_difficulties'].strip()
        objectiveOfCourse = request.POST['objectiveOfCourse'].strip()
        lanaguage = request.POST['lanaguage'].strip()
        tottal_credit_hour = request.POST['tottal_credit_hour'].strip()
        departements_selected = request.POST.getlist('departements')
        programs =request.POST.getlist('programs')

        if len(departements_selected)  == 0:
            print("xxxxxxxxxxxxxxxxxxxxxx 80 no departements selected pleasee select one  xxxxxxxxxxxxxx")
            return redirect('doh_course_info_edit', course_info)
        
        try:
            course_information = Courseinformations.objects.get( course_id = course_info)
            course_information.course_name = course_name
            course_information.level_of_difficulties = level_of_difficulties
            course_information.objectiveOfCourse = objectiveOfCourse
            course_information.lanaguage = lanaguage
            course_information.tottal_credit_hour = tottal_credit_hour
            course_information.programs = programs[0]
            dep = Department.objects.get(id = departements_selected[0])
            course_information.departement = dep

            course_information.save()
            print("xxxxxxxxxxxxxxxxxxxxxx  82 Successfully edited course information xxxxxxxxxxxxxx")
            return redirect('doh_course_management')
        except:
            print("xxxxxxxxxxxxx 81 Failed editing course information xxxxxxxxxxx")
        
    

        

         



    departements = Department.objects.all()

    current_course = Courseinformations.objects.get( course_id = course_info)

    selected_dep = current_course.departement
    
    context = {
        'selected_dep':selected_dep,
        'current_course':current_course,
        'departements':departements,
        'is_empty': len(departements)
    }

    return render(request, 'Doh/course_editing_page.html', context = context)

