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
    return render(request , 'Doh/personal_account_mgt.html', context=context)
