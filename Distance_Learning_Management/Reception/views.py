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


def fileTypeChecker(fileName , listofExetensions):
    loweredName = fileName
   
    
    for extension in listofExetensions:
        if loweredName.endswith(extension.lower()):
            return True
    
    return False


@login_required(login_url='base_login_page')
@school_registerar_only
def registerars_landing_page(request):
    return render(request, 'Reception/dashboard_for_reception_display_page.html')



@login_required(login_url='base_login_page')
@school_registerar_only
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
            print("XXXXXXXXXXXXXXXX 40 UPDATED registerar personal info XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('registerar_presonal_account_mgt')
        except Exception as e:
            print(e)
            print("XXXXXXXXXXXXXXXX    41 FAIL registerar personal account inf update   XXXXXXXXXXXXXXXXXXXXXXXX")
            return redirect('registerar_presonal_account_mgt')



    context = {
        'user_infn':user_object,
        'personal_info':current_employe_object
    }
    return render(request , 'Reception/personal_account_mgt.html', context=context)



@login_required(login_url='base_login_page')
@school_registerar_only
def registerar_logout(request):
    logout(request)
    return redirect('site_main_landing_page')

@login_required(login_url='base_login_page')
@school_registerar_only
def student_information_management_page(request):
    
    student_object = StudentInformation.objects.all()
    context = {
        'student_object':student_object,
        'is_empty': len(student_object)
    }
    return render(request, 'Reception/student_information_mgt.html',context=context)

@login_required(login_url='base_login_page')
@school_registerar_only
def student_information_inserting_page(request):

    if request.method == 'POST':
        first_name = request.POST['first_name'].strip()
        middle_name = request.POST['middle_name'].strip()
        last_name = request.POST['last_name'].strip()
        age = request.POST['age'].strip()
        country = request.POST['country'].strip()
        woreda = request.POST['woreda'].strip()
        street = request.POST['street'].strip()
        phone_number = request.POST['phone_number'].strip()
        profile_pictures = request.FILES['profile_pictures']
        email = request.POST['email'].strip()
        username = request.POST['username'].strip()
        cv = request.FILES['cv']
        choosed_dep = request.POST.getlist('departement')
        program = request.POST.getlist('program')
        
    
        listofImage = [".jpg",".png", ".jpeg", ".gif", ".bmp", '.tif' ]
        listOfPDFTypes = ['.DOC', '.DOCX','.PDF' ]

        extesionpdf   =  os.path.splitext(str(cv))
        extesionImg   =  os.path.splitext(str(profile_pictures))

        if fileTypeChecker(extesionpdf[1], listOfPDFTypes ):
            pass
        else:
            print("Document Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            print("tttttttttttttttttttt 1000 Error Mismatch in cv file format tttttttttttttttttttttttttt")
            return render(request, 'Reception/student_information_inserting_page.html')

        if fileTypeChecker(extesionImg[1], listofImage ):
            pass
        else:
            print("Image Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            print("tttttttttttttttttttt 1001 Error Mismatch in profile pic file format tttttttttttttttttttttttttt")
            return render(request, 'Reception/student_information_inserting_page.html')

        try:
            flag = True
            while flag:         
                randomeNumber = random.randint(1, 1000000000000000000)
                id_generated = f"ST{randomeNumber}"
                try:
                    id_generated = Employee.objects.get(employeeid = id_generated)
                except:
                    flag = False
                    break
                    
            try:
                departement = Department.objects.get(id = choosed_dep[0])
                course_information = Courseinformations.objects.filter(Q(programs = program[0]) & Q(departement = departement) )        

                if not len(course_information) > 0:  
                    raise Exception
        
            except Exception as e:
                print("-----------------------------")
                print(e)
                print("Make sure u add this message if the user got this ")
                print("xxxxxxxxxxxxxxxxxx 65 The departement student choosed with this program its not availabel so add this message xxxxxxxxxxxxxxxxxxxxxxxx")
                
                departement = Department.objects.all()
    
                bsc = Courseinformations.objects.filter(programs ='Bchelor Degree')
                msc = Courseinformations.objects.filter(programs ='Masters Degree')
                
                programs = dict()
                if len(bsc) > 0:
                    programs['Bchelor Degree'] = 'Bchelor Degree'
                if len(msc) > 0:  
                    programs['Masters Degree'] = 'Masters Degree'
                    
                context = {
                    'departement': departement,
                    'is_empty': len(departement),
                    'programs' : programs
                }
                return render(request, 'Reception/student_information_inserting_page.html', context=context)


            user_object = User.objects.create(
                username = username,
                password = username
            )
            user_object.set_password(username)
            user_object.save()


            student = StudentInformation.objects.create(
                userid = id_generated,
                firstname = first_name,
                middlename = middle_name,
                lastname = last_name,
                age = age,
                country = country,
                woredazone = woreda,
                streetkebele = street,
                phonenumber = phone_number,
                profilePicture = profile_pictures,
                student_cv_pdf_file = cv,
                email = email,
                userObject = user_object
            )

            my_group = Group.objects.get_or_create(name='Student') 
            my_group = Group.objects.get(name='Student')
            user_object.groups.add(my_group)
            StudentAcademicOption.objects.create(
                            student_id = student,
                            departement = departement,
                            programs = program[0]
                        )

            print('xxxxxxxxxxxxxxxxxxx 46 successfully registred student Info xxxxxxxxxxxxxxxxx') 
            return redirect('registerar_student_info_mgt')
        except Exception as e:
           print(e)
           print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx 45 Failed to store student info xxxxxxxxxxxxxxxxxxxx')
    
    departement = Department.objects.all()
   
    bsc = Courseinformations.objects.filter(programs ='Bchelor Degree')
    msc = Courseinformations.objects.filter(programs ='Masters Degree')
    programs = dict()
    if len(bsc) > 0:
        programs['Bchelor Degree'] = 'Bchelor Degree'
    if len(msc) > 0:  
        programs['Masters Degree'] = 'Masters Degree'
        
    context = {
        'departement': departement,
        'is_empty': len(departement),
        'programs' : programs
    }
    return render(request, 'Reception/student_information_inserting_page.html', context=context)

@login_required(login_url='base_login_page')
@school_registerar_only
def student_information_editing_page(request, stud_id):
    student = StudentInformation.objects.get(userid = stud_id)
    try:
        student_academic = StudentAcademicOption.objects.get(student_id = student.userid)
    except Exception as e:
        student_academic = []

    if request.method == 'POST':
        first_name = request.POST['first_name'].strip()
        middle_name = request.POST['middle_name'].strip()
        last_name = request.POST['last_name'].strip()
        age = request.POST['age'].strip()
        country = request.POST['country'].strip()
        woreda = request.POST['woreda'].strip()
        street = request.POST['street'].strip()
        phone_number = request.POST['phone_number'].strip()
        profile_pictures = request.FILES['profile_pictures']
        email = request.POST['email'].strip()
        username = request.POST['username'].strip()
        cv = request.FILES['cv']
        choosed_dep = request.POST.getlist('departement')
        program = request.POST.getlist('program')

        listofImage = [".jpg",".png", ".jpeg", ".gif", ".bmp", '.tif' ]
        listOfPDFTypes = ['.DOC', '.DOCX','.PDF' ]

        extesionpdf  =  os.path.splitext(str(cv))
        extesionImg  =  os.path.splitext(str(profile_pictures))

        if fileTypeChecker(extesionpdf[1], listOfPDFTypes ):
            pass
        else:
            print("Document Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            print("tttttttttttttttttttt 1000 Error Mismatch in cv file format tttttttttttttttttttttttttt")
            return render(request, 'Reception/student_information_inserting_page.html')

        if fileTypeChecker(extesionImg[1], listofImage ):
            pass
        else:
            print("Image Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            print("tttttttttttttttttttt 1001 Error Mismatch in profile pic file format tttttttttttttttttttttttttt")
            return render(request, 'Reception/student_information_inserting_page.html')

        try:
           
            try:
                departement_ = Department.objects.get(id = choosed_dep[0])
                course_information = Courseinformations.objects.filter(Q(programs = program[0]) & Q(departement = departement_) )        

                if not len(course_information) > 0:  
                    raise Exception
        
            except Exception as e:
                print("-----------------------------")
                print(e)
                print("Make sure u add this message if the user got this ")
                print("xxxxxxxxxxxxxxxxxx 66 The departement student choosed with this program its not availabel so add this message xxxxxxxxxxxxxxxxxxxxxxxx")

                return redirect('registerar_student_info_edit', stud_id)


            student.firstname = first_name
            student.middlename = middle_name
            student.lastname =last_name
            student.age = age
            student.country = country
            student.woredazone = woreda
            student.streetkebele = street
            student.phonenumber = phone_number
            student.profilePicture = profile_pictures
            student.student_cv_pdf_file = cv
            student.email = email

            userobject = student.userObject
            userobject.username  =username
            userobject.save()
            student.userObject = userobject

            if isinstance(student_academic, list):
                StudentAcademicOption.objects.create(
                    student_id = student,
                    departement = departement_,
                    programs = program[0]
                    )
            else:   
                student_academic.departement = departement_
                student_academic.programs = program[0]
                student_academic.save()


            student.save()
            print('xxxxxxxxxxxxxxxxxxxxxxxxx 48 Successfully Updated Student Info xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            return redirect('registerar_student_info_mgt')
        except Exception as e:
            print(e)
            print('xxxxxxxxxxxxxxxx 49 failed to updated the student Info xxxxxxxxxxxxxxxxxxxx')
            return redirect('registerar_student_info_edit', stud_id)            
            
    

    departement = Department.objects.all()
   
    bsc = Courseinformations.objects.filter(programs ='Bchelor Degree')
    msc = Courseinformations.objects.filter(programs ='Masters Degree')
    programs = dict()
    if len(bsc) > 0:
        programs['Bchelor Degree'] = 'Bchelor Degree'
    if len(msc) > 0:  
        programs['Masters Degree'] = 'Masters Degree'
 

    context = {
        'departement': departement,
        'is_empty': len(departement),
        'programs' : programs,
        'student':student,
        'student_academic':student_academic,
        'student_academic_empty': 1 if student_academic is not None and student_academic != [] else len(student_academic)
    }
    return render(request, 'Reception/student_information_mgt_edit_page.html', context= context)

@login_required(login_url='base_login_page')
@school_registerar_only
def student_information_deleting_page(request, stud_id):
    try:

        student = StudentInformation.objects.get(userid = stud_id)
        
        student_academic = StudentAcademicOption.objects.get(student_id = student)
        student_academic.delete()

        
        userobject =  student.userObject
        userobject.delete()
        student.delete()

        

        print('xxxxxxxxxxxxxxxxxxx 50 Successfully deleted student info xxxxxxxxxxxxxxxxxxxxxxxx')
        
    except Exception as e:
        print(e)
        print('xxxxxxxxxxxxxxxxxxxxx 51 Failed to deleted student Info xxxxxxxxxxxxxxxx')
    return redirect('registerar_student_info_mgt')


@login_required(login_url='base_login_page')
@school_registerar_only
def photo_taken_page(request, stud_id):
    
    context = {
        'student_id': stud_id
    }
    return render(request, 'Reception/pcture_taking_page.html', context = context)

@login_required(login_url='base_login_page')
@school_registerar_only
def  registerar_train_model(request):

    return render(request, 'Reception/modelTraningPage.html')


@login_required(login_url='base_login_page')
@school_registerar_only
def registerar_duedate_page(request):
    
    if request.method == "POST":
        due_date = request.POST['due_date']
        departement_id = request.POST['departement_id']
        try:
            if str(due_date).strip() == "":
                raise Exception
            
            parsed_day = int(due_date)
            
            departement = Department.objects.get( id = departement_id)

            try:
                due_date = DueDatePayemenet.objects.get( departement = departement)
                due_date.due_date = parsed_day
                due_date.save()
            except:
                DueDatePayemenet.objects.create(
                    departement = departement,
                    due_date = parsed_day
                )
            
            print("xxxxxxxxxxxxx 65 Due Date is saved successfully xxxxxxxxxxxx")
            return redirect('due_date_management')
        except Exception as e:
            print(e)
            print("xxxxxxxxxxxxx 65 Due Date is Failed to be saved xxxxxxxxxxxx")
            return redirect('due_date_management')
        
    departement = Department.objects.all()

    mapped  = []
    for dep in departement:
        try:
            due_date = DueDatePayemenet.objects.get( departement = dep)
            mapped.append(due_date)
        except:
            pass
        
    context = {
        'departement':departement,
        'is_empty':len(departement),
        'mapped':mapped,
        'is_empty_mapped':len(mapped)
    }
    return render(request, 'Reception/payement_due_date_page.html', context = context)
