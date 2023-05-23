from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators  import *
from .models import Employee,RoleInSchool,Faculty,Department,Courseinformations,PriceForDepartements


import random
# Create your views here.


def school_admin_landingpage(request):
    if request.user.is_authenticated: # if alrady logged in
        try:
            group = request.user.groups.all()[0].name
            if str(group).strip().lower() == 'School_Manager'.lower():
                return redirect('admin_main_landing_page')
        except:
            logout(request)
            
    return render(request, "School_Admin/index.html")

def login_page(request):
    if request.user.is_authenticated: # if alrady logged in
        group = request.user.groups.all()[0].name
        if str(group).strip().lower() == 'School_Manager'.lower():
            return redirect('admin_main_landing_page')
        

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

            my_group = Group.objects.get_or_create(name='Teacher') 
            my_group = Group.objects.get(name='Teacher')
            user_object.groups.add(my_group) 


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


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_manage_registerar(request):
    registerar_roles = RoleInSchool.objects.filter(employee_role = 'Registrar')

    context = {
        'staff_object': registerar_roles,
        'is_empty' : len(registerar_roles)
    }
    return render(request, 'School_Admin/registerar_information_mgt.html',context=context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_registerar_info_insert(request):
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
            id_generated = f"RG{randomeNumber}"
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


            role = RoleInSchool.objects.create(employee = employee, employee_role = 'Registrar')
            role.save()

            my_group = Group.objects.get_or_create(name='Registerar') 
            my_group = Group.objects.get(name='Registerar')
            user_object.groups.add(my_group) 

            print("xxxxxxxxxxxxx 8 success Registering registerar")
            return redirect('view_list_registerar')

        except Exception as e:
            print(e)
            # return fail message with it 
            print("XXXXXXXX 9 Fail registering registerar XXXXXXXXXXXXXXX")
        

        

    return render(request, 'School_Admin/registerar_information_inserting_page.html')

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_registerar_delete(request, eployee_id):
    try:
        registerar_id = Employee.objects.get(employeeid = eployee_id)
        user_object = registerar_id.userObject
        user_object.delete()
        registerar_id.delete()
        
        print("xxxxxx  9 successfully delete info Registerar xxxxxx")
        return redirect('view_list_registerar')
    except Exception as e:
        print(e)
        print("xxxxxxx 10 Failed to delete Registerar information xxxxxxxxxx")
        return redirect('view_list_registerar')

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_regiseterar_information_edit(request, eployee_id):
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
                print('XXXXXXXXXXXXXXXXXXXXXX 11 Successfully updated regiseterar info XXXXXXXXXXXXXXXXXXXXXX')
                return redirect('view_list_registerar')
                
            except:
                print("XXXXXXXXXXXXXXXXXXXXX 12 Fail to update registerar information xxxxxxxxxxxxxxxx")



        
        context = {
            'staff_info':teacher_id,
            'user_object':user_object
        }

        return render(request, 'School_Admin/registerar_information_editing_page.html', context = context)
    except Exception as e:
        print("xxxxxxx 15 Failed to delete registerar information xxxxxxxxxx")
        return redirect('view_list_registerar')


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_list_of_adminstrations_staffs(request):

    admins_object = RoleInSchool.objects.filter(employee_role = 'Admin')
    
    context = {
        'admins_object': admins_object,
        'is_empty' : len(admins_object)
    }

    return render(request, 'School_Admin/school_admins_listViewPage.html', context=context)


@login_required(login_url='admin_login_page')
@school_manager_only
def school_admin_registering_page(request):
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
            id_generated = f"AD{randomeNumber}"
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


            role = RoleInSchool.objects.create(employee = employee, employee_role = 'Admin')
            role.save()

            my_group = Group.objects.get_or_create(name='School_Manager') 
            my_group = Group.objects.get(name='School_Manager')
            user_object.groups.add(my_group) 

            print("xxxxxxxxxxxxx 16 success Registering Admin")
            return redirect('admin_staffs_display_page')

        except Exception as e:
            print(e)
            # return fail message with it 
            print("XXXXXXXX 17 Fail registering  Admin XXXXXXXXXXXXXXX")
        

        

    return render(request, 'School_Admin/school_admin_new_admin_regisetering_page.html')

@login_required(login_url='admin_login_page')
@school_manager_only
def school_admin_account_delete(request, eployee_id):
    try:
        admin_id = Employee.objects.get(employeeid = eployee_id)
        user_object = admin_id.userObject
        user_object.delete()
        admin_id.delete()
        print("xxxxxx  19 successfully delete info school Admin  xxxxxx")
        return redirect('admin_staffs_display_page')
    except Exception as e:
        print(e)
        print("xxxxxxx 20 Failed to delete school admin information xxxxxxxxxx")
        return redirect('admin_staffs_display_page')


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_manage_faculty(request):
    stored_faculty = Faculty.objects.all()
    context = {
        "faculty_info" :stored_faculty, 
        "is_empty": len(stored_faculty)
    }
    
    return render(request, 'School_Admin/faculty_list_admin_view_page.html', context = context)

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_new_faculty_register(request):
    
    if request.method == "POST":
        name_of_faculty = request.POST['faculty_name'].strip()
        choosen_teacher = request.POST['choosen_teacher'].strip()

        try:
            Faculty.objects.create(facult_adminstrator =Employee.objects.get(employeeid = choosen_teacher ) , full_faculty_name = name_of_faculty)

            print("xxxxxxxxxxxxxxxxxxx 23 successfull storing new faculty xxxxxxxxxxxxxxxxxxxxxxxx")
            return redirect('admin_manage_faculty_info')
        except:
            print("xxxxxxxxxxxxxxxxxxxxx  22  Failed to store new fauculty infor xxxxxxxxxxxxx")
        
        

    current_employees_with_teacher_role = RoleInSchool.objects.filter(employee_role = 'Teacher')
    # if teacher is already have assigned to faculty
    
    final_list = []
    for teacher in current_employees_with_teacher_role:
        try:
            Faculty.objects.get(facult_adminstrator = teacher.employee)
        except:
            final_list.append(teacher)

    context = {
        'availabel_teachers' :final_list,
        'is_empty':len(final_list)
    }


    return render(request, 'School_Admin/faculty_register_new_faculty_info.html', context= context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_view_faculty_info_delete(request, faculty_id):
    try:
        faculty = Faculty.objects.get(id = faculty_id)
        faculty.delete()
        
        print("xxxxxxxxxxxxxx 25 successfully deleted faculty info xxxxxxxxxxxx")
    except:
        print("xxxxxxxxxxxxxxx 24 Failed to delete faculthy info  xxxxxxxxxxxxxxxxx")
    return redirect('admin_manage_faculty_info')


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_view_update_faculty_info(request, faculty_id):
    
    if request.method == "POST":
        name_of_faculty = request.POST['faculty_name'].strip()
        choosen_teacher = request.POST['choosen_teacher'].strip()
        faculty = Faculty.objects.get(id = faculty_id)
    
        faculty.full_faculty_name = name_of_faculty
        faculty.facult_adminstrator = Employee.objects.get(employeeid = choosen_teacher )

        try:
            faculty.save()
            print("xxxxxxxxx 27 successfully update the fauclty data xxxxxxxxx")
        except:
            print("xxxxxxxxxxx 26 Failes to update faculty info xxxxxxxxxxxx")
        return redirect('admin_manage_faculty_info')

    try:   
        faculty = Faculty.objects.get(id = faculty_id)
        
        final_list = []
        teachers = RoleInSchool.objects.filter(employee_role = 'Teacher')
        
        for teacher in teachers:
            try:
                if teacher.employee.employeeid == faculty.facult_adminstrator.employeeid:
                    raise Exception
                
                Faculty.objects.get(facult_adminstrator = teacher.employee)
            except Exception:
                final_list.append(teacher)

        context = {
            "faculty_info":faculty,
            "availabel_teachers": final_list
        }
        return render(request, 'School_Admin/faculty_info_editing_page.html', context = context)
    except Exception as e:
        
        print(e)
        return redirect('admin_manage_faculty_info')


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_manage_departement(request):
    departements = Department.objects.all()
    context = {
        'departements':departements,
        'is_empty': len(departements)
    }
    return render(request, 'School_Admin/departement_info_mgt.html', context= context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_manage_departement_info_insert(request):

    if request.method == "POST":
        name_of_department = request.POST['name_of_department'].strip()
        faculty_choosen  = request.POST['faculty'].strip()
        doh = request.POST['doh'].strip()

        try:
            Department.objects.create(
                name_of_department = name_of_department ,
                faculty_info = Faculty.objects.get(id =faculty_choosen ),
                departement_head = Employee.objects.get(employeeid = doh)
            )
            print("xxxxxxxxxxxxxxxxxx  29 successful inserting  xxxxxxxxxxxxxxxxxxx")
            return redirect('admin_manage_departement_info')
        except Exception as e:
            print("xxxxxxxxxxxxxxxxxx 28 Fail to insert departement data xxxxxxxxxxxxxxxxxxx")
        
       
    current_employees_with_teacher_role = RoleInSchool.objects.filter(employee_role = 'Teacher')
    
    
    final_list = []
    for teacher in current_employees_with_teacher_role:
        try:
            Faculty.objects.get(facult_adminstrator = teacher.employee)
            
        except:
            try:
                Department.objects.get(departement_head = teacher.employee)
            except:
                final_list.append(teacher)

    final_list2 = []
    
    for faculty in Faculty.objects.all():
        
        try:
            Department.objects.get(faculty_info = faculty)
        except:
            final_list2.append(faculty)

    context = {
        'availabel_teachers' :final_list,
        'is_empty':len(final_list),
        'availabel_faculties' :  final_list2,
        "is_empty2":len(final_list2)
    }

    return render(request, 'School_Admin/departement_registering_page.html', context = context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_delete_departement_information(request, departement_id):
    try:
        department = Department.objects.get(id = departement_id)
        department.delete()
        print("xxxxxxxxxxxxxx 30 successfully deleted departement info xxxxxxxxxxxx")
    except:
        print("xxxxxxxxxxxxxxx 31 Failed to delete departement info  xxxxxxxxxxxxxxxxx")
    return redirect('admin_manage_departement_info')

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_editing_departement_info(request, departement_id):
    
    if request.method == "POST":
        name_of_department = request.POST['name_of_department'].strip()
        faculty_choosen  = request.POST['faculty'].strip()
        doh = request.POST['doh'].strip()

        current_to_be_edit_dep = Department.objects.get(id = departement_id)

        try:

            current_to_be_edit_dep.name_of_department = name_of_department
            current_to_be_edit_dep.faculty_info = Faculty.objects.get(id = faculty_choosen )
            current_to_be_edit_dep.departement_head = Employee.objects.get(employeeid = doh)
            current_to_be_edit_dep.save()
            
            print("xxxxxxxxxxxxxxxxxx  31 successful Updating  xxxxxxxxxxxxxxxxxxx")
            return redirect('admin_manage_departement_info')
        except Exception as e:
            print(e)
            print("xxxxxxxxxxxxxxxxxx 32 Fail to Update departement data xxxxxxxxxxxxxxxxxxx")
        
       
    current_employees_with_teacher_role = RoleInSchool.objects.filter(employee_role = 'Teacher')
    
    
    final_list = []
    for teacher in current_employees_with_teacher_role:
        try:
            Faculty.objects.get(facult_adminstrator = teacher.employee)
            
        except:
            try:
                dep = Department.objects.get(departement_head = teacher.employee)

                if str(dep.id) == str(departement_id):
                    raise Exception
            except Exception:
                final_list.append(teacher)

    final_list2 = []
    
    for faculty in Faculty.objects.all():
        
        try:
            dep = Department.objects.get(faculty_info = faculty)
            if str(dep.id) == str(departement_id):
                    raise Exception
        except Exception:
            final_list2.append(faculty)

    current_to_be_edit_dep = Department.objects.get(id = departement_id)
    context = {
        'availabel_teachers' :final_list,
        'is_empty':len(final_list),
        'availabel_faculties' :  final_list2,
        "is_empty2":len(final_list2),
        "current_departement_info":current_to_be_edit_dep
    }

    return render(request, 'School_Admin/departement_info_editing_page.html', context = context)



@login_required(login_url='admin_login_page')
@school_manager_only
def admin_coures_information_management(request):

    course_infomations = Courseinformations.objects.all()
    
    context = {
        'course_infomations': course_infomations,
        'is_empty': len(course_infomations)
    }
    return render(request, 'School_Admin/course_info_management_by_admin.html', context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_course_information_inserting(request):
    if request.method == "POST":
        course_name = request.POST['course_name'].strip()
        level_of_difficulties = request.POST['level_of_difficulties'].strip()
        objectiveOfCourse = request.POST['objectiveOfCourse'].strip()
        lanaguage = request.POST['lanaguage'].strip()
        tottal_credit_hour = request.POST['tottal_credit_hour'].strip()
        departements_selected = request.POST.getlist('departements')
        programs =request.POST.getlist('programs')

        if len(departements_selected)  == 0:
            print("xxxxxxxxxxxxxxxxxxxxxx 34.3 no departements selected please  xxxxxxxxxxxxxx")
            return redirect('course_information_view_management')
            
   
        for program in programs:
            for dep in departements_selected:
                departement_ = Department.objects.get(id = dep)
                

                flag = True
                while flag:         
                    randomeNumber = random.randint(1, 100000000000000000000)
                    id_generated = f"{randomeNumber}"
                    try:
                        id_generated = Courseinformations.objects.get(course_id = id_generated)
                    except:
                        flag = False
                        break
                

                
                try:
                    course_information = Courseinformations.objects.create(
                        course_id = id_generated,
                        course_name = course_name,
                        level_of_difficulties = level_of_difficulties,
                        objectiveOfCourse = objectiveOfCourse,
                        lanaguage = lanaguage,
                        tottal_credit_hour = tottal_credit_hour,
                        departement = departement_,
                        programs = program
                    )
                    print('xxxxxxxxxxxxxxxxx 35 Successfully inserted course info xxxxxxxxxxxxxxxxxxxxx')
                    
                except Exception as e:
                    print(e)
                    print("xxxxxxxxxxxxxxxxxxxxxx 34 Failed to inserte course info")

        return redirect('course_information_view_management')


    departements = Department.objects.all()

    context = {
        'departements':departements,
        'is_empty': len(departements)
    }
    
    return render(request, 'School_Admin/course_info_inserting_page.html', context = context)

@login_required(login_url='admin_login_page')
@school_manager_only
def admin_course_information_deleting(request, course_id):
    try:
        course_object = Courseinformations.objects.get(course_id = course_id)
        course_object.delete()
        print("xxxxxxxxxxxxxx 34 successfully deleted Course info xxxxxxxxxxxx")
    except:
        print("xxxxxxxxxxxxxxx 35 Failed to delete Course info  xxxxxxxxxxxxxxxxx")
    
    return redirect('course_information_view_management')


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_departement_price_fixation(request):

    price_of_departements = PriceForDepartements.objects.all()
    context = {
        'price_of_departements' : price_of_departements,
        'is_empty': len(price_of_departements)
    }
    return render(request, 'School_Admin/price_fixation_management_page.html', context = context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_departement_price_inserting(request):
    
    if request.method == 'POST':
        school_fee = request.POST['school_fee'].strip()
        departements_id = request.POST['departement_selected'].strip()

        try:
            PriceForDepartements.objects.create(
                department = Department.objects.get(id = departements_id),
                price = float(school_fee)
            )
            print("xxxxxxxxxxxxxxx 36 Sucessfully insert price for departement  xxxxxxxxxxxxxxxx")
            return redirect('admin_manage_departement_price')
        except Exception as e:
            print(e)
            print('xxxxxxxxxxxxxx 35 Failed to insert school fee for students xxxxxxxx ')

        

    all_dep = Department.objects.all()
    
    
    final_list_holder = []
    for dep in all_dep:
        try:
            PriceForDepartements.objects.get(department = dep)
        except:
            final_list_holder.append(dep)
    context = {
        'departements':final_list_holder,
        'is_empty':len(final_list_holder)
    }
        
    return render(request, 'School_Admin/price_fixation_inserting_page.html',context = context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_departement_price_editing(request, price_id):

    price_object = PriceForDepartements.objects.get(id = price_id)
    if request.method == "POST":
        school_fee = request.POST['school_fee'].strip()
        departements_id = request.POST['departement_selected'].strip()

        try:

            price_object.department = Department.objects.get(id = departements_id)
            price_object.price = float(school_fee)
            price_object.save()
           
            print("xxxxxxxxxxxxxxx 38 Sucessfully updated price for departement  xxxxxxxxxxxxxxxx")
            return redirect('admin_manage_departement_price')
        except Exception as e:
            print(e)
            print('xxxxxxxxxxxxxx 37 Failed to update school fee for students xxxxxxxx ')

        
    

    all_dep = Department.objects.all()
    
    
    final_list_holder = []
    for dep in all_dep:
        try:
            
            PriceForDepartements.objects.get(department = dep)
            if price_object.department.id == dep.id:
                final_list_holder.append(dep)
        except:
            final_list_holder.append(dep)

    context = {
        'departements':final_list_holder,
        'is_empty':len(final_list_holder),
        'price_object':price_object
    }

    return render(request, 'School_Admin/price_fixation_editing_page.html', context = context)


@login_required(login_url='admin_login_page')
@school_manager_only
def admin_departement_price_delete(request, price_id):
    try:
        price_object = PriceForDepartements.objects.get(id = price_id)
        price_object.delete()
        print("xxxxxxxxxxxxxx 39 successfully deleted Price info xxxxxxxxxxxx")
    except:
        print("xxxxxxxxxxxxxxx 35 Failed to delete Price info  xxxxxxxxxxxxxxxxx")
    
    return redirect('admin_manage_departement_price')
