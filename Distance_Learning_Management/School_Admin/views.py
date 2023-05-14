from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators  import *
from .models import Employee,RoleInSchool


import random
# Create your views here.


def school_admin_landingpage(request):
    return render(request, "School_Admin/index.html")

def login_page(request):
    if request.method == 'POST':
        user_name = request.POST['username'].strip()
        password =  request.POST['password'].strip()
        user = authenticate(request, username=user_name,  password=password)

        if user is not None :
            login(request, user)
            if request.user.is_authenticated :
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                    if str(group).strip().lower() == 'School_Manager'.lower():
                        return redirect('admin_main_landing_page')
                                      
                logout(request)
                return redirect('landing_page_school_admin')
        else:
            return redirect('landing_page_school_admin')
            
    return render(request, 'School_Admin/login.html')

@login_required(login_url='admin_login_page')
@school_manager_only
def school_admin_logout(request):
    logout(request)
    return redirect('landing_page_school_admin')

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_main_landing_page(request):
    user_object = User.objects.get(username=request.user)
    return render(request, 'School_Admin/landing_page.html')

@login_required(login_url='admin_login_page')
@school_manager_only
def school_admin_personal_account(request):
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
            print("XXXXXXXXXXXXXXXX 2 UPDATED XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('admin_personal_account')
        except Exception as e:
            print(e)
            print("XXXXXXXXXXXXXXXX    1 FAIL   XXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('admin_personal_account')



    context = {
        'user_infn':user_object,
        'personal_info':current_employe_object
    }
    return render(request , 'School_Admin/personal_account.html', context=context)

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_manage_teacher(request):  
    teacher_roles = RoleInSchool.objects.filter(employee_role = 'Teacher')

    
    context = {
        'teacher_object': teacher_roles,
        'is_empty' : len(teacher_roles)
    }
    return render(request, 'School_Admin/teacher_information_mgt.html',context=context)

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_teacher_inserting_information(request):
    

    if request.method == "POST":
        first_name = request.POST['firstname'].strip()
        middle_name = request.POST['middlename'].strip()
        last_name = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        gender = request.POST['gender'].strip()
        phone_number = request.POST['phonenumber'].strip()
        address = request.POST['address'].strip()
        email = request.POST['email'].strip()

        
        flag = True
        while flag:         
            randomeNumber = random.randint(1, 1000000000000000000)
            id_generated = f"TR{randomeNumber}"
            try:
                id_generated = Employee.objects.get(employeeid = id_generated)
            except:
                flag = False
                break

        try:
            user_object = User.objects.create(
                username = username,
                password = username
            )
            user_object.set_password(username)
            user_object.save()

            employee = Employee.objects.create(
                    firstname = first_name,
                    middlename = middle_name,
                    lastname = last_name,
                    username = username,
                    gender = gender,
                    phonenumber = phone_number,
                    address = address,
                    email = email,
                    userObject = user_object,
                    employeeid = id_generated,
            )

            employee.save()


            role = RoleInSchool.objects.create(employee = employee, employee_role = 'Teacher')
            role.save()

            print("xxxxxxxxxxxxx 4 success Registering teacher")
            return redirect('view_list_teachers')

        except Exception as e:
            print(e)
            # return fail message with it 
            print("XXXXXXXX 3 Fail registering teacher XXXXXXXXXXXXXXX")
        



        

    return render(request, 'School_Admin/teacher_information_inserting_page.html')

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_teacher_information_deleting_url(request, eployee_id):
    try:
        teacher_id = Employee.objects.get(employeeid = eployee_id)
        user_object = teacher_id.userObject
        user_object.delete()
        teacher_id.delete()
        print("xxxxxx  6 successfully delete info teacher xxxxxx")
        return redirect('view_list_teachers')
    except Exception as e:
        print(e)
        print("xxxxxxx 5 Failed to delete teacher information xxxxxxxxxx")
        return redirect('view_list_teachers')

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_teacher_information_editing_url(request, eployee_id):
    try:
        teacher_id = Employee.objects.get(employeeid = eployee_id)
        user_object = teacher_id.userObject
        
        if request.method == "POST":
            first_name = request.POST['firstname'].strip()
            middle_name = request.POST['middlename'].strip()
            last_name = request.POST['lastname'].strip()
            username = request.POST['username'].strip()
            gender = request.POST['gender'].strip()
            phone_number = request.POST['phonenumber'].strip()
            address = request.POST['address'].strip()
            email = request.POST['email'].strip()
            
            teacher_id.firstname = first_name
            teacher_id.middlename = middle_name
            teacher_id.lastname = last_name
            teacher_id.username = username
            teacher_id.gender = gender
            teacher_id.phonenumber = phone_number
            teacher_id.address = address
            teacher_id.email = email
            user_object.username = username

            try:
                user_object.save()
                teacher_id.save()
                print('XXXXXXXXXXXXXXXXXXXXXX 7 Successfully updated XXXXXXXXXXXXXXXXXXXXXX')
                return redirect('view_list_teachers')
                
            except:
                print("XXXXXXXXXXXXXXXXXXXXX 6 Fail message to update teacher information xxxxxxxxxxxxxxxx")



        
        context = {
            'teacher_info':teacher_id,
            'user_object':user_object
        }

        return render(request, 'School_Admin/teacher_information_editing_page.html', context = context)
    except Exception as e:
        print(e)
        print("xxxxxxx 5 Failed to delete teacher information xxxxxxxxxx")
        return redirect('view_list_teachers')










