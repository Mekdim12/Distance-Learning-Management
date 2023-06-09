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
from .forms import *

from django.contrib import messages
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
            'msc_students':msc_students,
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


@login_required(login_url='base_login_page')
@school_teacher_only
def manage_course_information_teacher(request):

    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    availabel_course_list = TeacherToCourseMapping.objects.filter(teacher = current_employe_object)
    
    availabel_list_courses_list_final = []

    for map in availabel_course_list:
        [availabel_list_courses_list_final.append(course) for course in map.course_info.all()]
    
    context = {
        'course_list':availabel_list_courses_list_final,
        'is_empty':len(availabel_list_courses_list_final) > 0
    }
    return render(request, 'Teacher/course_management_main_page.html', context = context)


@login_required(login_url='base_login_page')
@school_teacher_only
def course_specific_management_page(request, course_id):
    # fetch list of course inserted using this teachere only for crud
    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object) 
    coursecontetns = MainCoursecontentdetailcontent.objects.filter( Q(courseid = Courseinformations.objects.get(course_id = course_id )) & Q(course_creator = current_employe_object))
    
    context = {
        'course_id':course_id,
        'coursecontetns':coursecontetns,
        'is_empty': len(coursecontetns) > 0
    }
    return render(request, 'Teacher/course_specific_mgt_page.html', context = context)


@login_required(login_url='base_login_page')
@school_teacher_only
def course_specific_main_content_inserting_page(request, course_id):
    
    if request.method == "POST":
        user_object = User.objects.get(username=request.user)
        current_employe_object = Employee.objects.get(userObject = user_object)

        listofAudioType = ['.MP3', '.AAC', '.FLAC ', '.ALAC', '.WAV', '.AIFF', '.DSD', '.PCM','.OGG']
        listOfVideoType = ['.MP4','.MOV', '.WMV','.AVI', '.AVCHD', '.FLV', '.F4V', '.SWF', 'MKV', 'WEBM', '.HTML5', '.MPEG-2']
        listOfPDFTypes = ['.DOC', '.DOCX', '.ODT','.PDF', '.XLSX', '.XLS', '.ODS', '.PPT','.PPTX','.TXT' ]
 
        audio = request.FILES['audio']
        video = request.FILES['video']
        pdf = request.FILES['pdf']
        notes = request.POST['notes']
        topic = request.POST['topic']

        extesionaudio = os.path.splitext(str(request.FILES['audio']))
        extesionvideo = os.path.splitext(str(request.FILES['video']))
        extesionpdf   =  os.path.splitext(str(request.FILES['pdf']))
        
        
        
        if fileTypeChecker(extesionpdf[1], listOfPDFTypes ):
            pass
        else:
            print("Document Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            return redirect('course_specific_main_content_inserting_page', course_id )
        
        if fileTypeChecker(extesionaudio[1], listofAudioType ):
            pass
        else:
            print("audio file mistmatch")
            # display error message tells user to change the file typeuse for audi file
            return redirect('course_specific_main_content_inserting_page',course_id )
        
        if fileTypeChecker(extesionvideo[1], listOfVideoType ):
            pass
        else:
            print("Video File Mistmatch")
            # display error message tells user to change the file typeuse for video file
            return redirect('course_specific_main_content_inserting_page', course_id )

        try:
            course_object = Courseinformations.objects.get(course_id = course_id)
            CourseContentDetail = MainCoursecontentdetailcontent(
                    courseid = course_object,
                    pdf = pdf,
                    audio = audio,
                    video = video,
                    notes = notes,
                    topic = topic,
                    course_creator = current_employe_object
                )
            CourseContentDetail.save()
            return redirect('specific_course_information_mgt_by_teacher',  course_id)
        except Exception as er:
            print(er)
            print("xxxxxxxxxxxxxxxxxx Failed to upload main course content ERROR CODE 102 -------------Teacher xxxxx")



    forms = MainCoursecontentdetailcontentForm()
    context = {
        "form":forms,
        'course_id':course_id,
    }
    return render(request, "Teacher/course_material_inserting_page.html", context = context)


@login_required(login_url='base_login_page')
@school_teacher_only
def course_specific_main_content_preview_and_update_page(request,course_id, content_id):

    detailCourseInformation = MainCoursecontentdetailcontent.objects.get(id=content_id )

    if request.method == "POST":
        
        listofAudioType = ['.MP3', '.AAC', '.FLAC ', '.ALAC', '.WAV', '.AIFF', '.DSD', '.PCM','.OGG']
        listOfVideoType = ['.MP4','.MOV', '.WMV','.AVI', '.AVCHD', '.FLV', '.F4V', '.SWF', 'MKV', 'WEBM', '.HTML5', '.MPEG-2']
        listOfPDFTypes = ['.DOC', '.DOCX', '.ODT','.PDF', '.XLSX', '.XLS', '.ODS', '.PPT','.PPTX','.TXT' ]
 
        audio = request.FILES['audio']
        video = request.FILES['video']
        pdf = request.FILES['pdf']
        notes = request.POST['notes']
        topic = request.POST['topic']


       
       
        extesionaudio = os.path.splitext(str(request.FILES['audio']))
        extesionvideo = os.path.splitext(str(request.FILES['video']))
        extesionpdf  = os.path.splitext(str(request.FILES['pdf']))
        
        
        
        if fileTypeChecker(extesionpdf[1], listOfPDFTypes ):
            pass
        else:
            print("Document Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            return redirect('course_specific_main_content_preview_update_page', course_id , content_id )
        
        if fileTypeChecker(extesionaudio[1], listofAudioType ):
            pass
        else:
            print("audio fiel mistmatch")
            # display error message tells user to change the file typeuse for audi file
            return redirect('course_specific_main_content_preview_update_page', course_id , content_id )
        
        if fileTypeChecker(extesionvideo[1], listOfVideoType ):
            pass
        else:
            print("Video File Mistmatch")
            # display error message tells user to change the file typeuse for video file
            return redirect('course_specific_main_content_preview_update_page', course_id , content_id )


        try:
            # check if the new file is different from the previous one

            detailCourseInformation.pdf = pdf
            detailCourseInformation.audio = audio
            detailCourseInformation.video = video
            detailCourseInformation.notes = notes
            detailCourseInformation.topic = topic

            detailCourseInformation.save()

            return redirect('specific_course_information_mgt_by_teacher',  course_id)

        except Exception as er:
            print(er)
            print("xxxxxxxxxxxxx Fialed To Update Course Information ERROR CODE 33 -------------Teacher xxxxxxxxxxxxxxx")



    
    valusToPopulated = {
        "pdf":detailCourseInformation.pdf,
        "audio":detailCourseInformation.audio,
        "video":detailCourseInformation.video,
        "notes":detailCourseInformation.notes,
        "topic":detailCourseInformation.topic,
    }

    form = MainCoursecontentdetailcontentForm(valusToPopulated)
    
    context = {
        'courseid':course_id,
        'contentId':content_id,
        'form':form,
        'detailInfn':detailCourseInformation,
    }


    return render(request, 'Teacher/course_information_displaying_course_material.html', context = context)


@login_required(login_url='base_login_page')
@school_teacher_only
def teacher_examination_mgt_course_view_page(request):
    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    availabel_course_list = TeacherToCourseMapping.objects.filter(teacher = current_employe_object)
    
    availabel_list_courses_list_final = []

    for map in availabel_course_list:
        [availabel_list_courses_list_final.append(course) for course in map.course_info.all()]
    
    context = {
        'course_list':availabel_list_courses_list_final,
        'is_empty':len(availabel_list_courses_list_final) > 0
    }

    return render(request, 'Teacher/examination_mgt_page.html', context = context)

@login_required(login_url='base_login_page')
@school_teacher_only
def exam_management_for_course_specific(request, course_id):
    #  list of examination added will be listed here by this teacher
    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    tf_questions = Examinationsection.objects.filter(Q(teacherid = current_employe_object) & Q(type = 'TF') & Q(courseinfn = Courseinformations.objects.get(course_id = course_id ))  )
    mc_questions = Examinationsection.objects.filter(Q(teacherid = current_employe_object) & Q(type = 'MC') & Q(courseinfn = Courseinformations.objects.get(course_id = course_id ))  )
    fb_questions = Examinationsection.objects.filter(Q(teacherid = current_employe_object) & Q(type = 'FB') & Q(courseinfn = Courseinformations.objects.get(course_id = course_id ))  )
    
    
    context = {
        'course_id':course_id,
        'tf_questions':tf_questions,
        'is_tf_empty':len(tf_questions) > 0,
        'mc_questions':mc_questions,
        'is_mc_empty':len(mc_questions)>0,
        'fb_questions':fb_questions,
        'is_fb_empty':len(fb_questions)>0
    }

    return render(request, 'Teacher/examination_information_course_specific_mgt_page.html', context = context)


@login_required(login_url='base_login_page')
@school_teacher_only
def exam_management_question_and_answer_inserting_page(request, course_id):

    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    if request.method == "POST":
        list_of_tf_question = request.POST.getlist('tableofContent_tf')
        list_of_mp_question = request.POST.getlist('tableofContent_mp')
        list_of_fb_question = request.POST.getlist('tableofContent_fb')

        QuestionWithAns_tf = {}
        QuestionWithAns_mp = {}
        QuestionwithChoices_mp = {}
        QuestionWithAns_fb = {}


        if len(list_of_tf_question) > 0:
            if len(request.POST["counter_tf"])>0:
                maxNumberOfPossibleAnswer = int(request.POST["counter_tf"])
            else:
                maxNumberOfPossibleAnswer = 1
            
            removed_tf = request.POST["removed_tf"] 

            counter = 1
            questionindex = 0

            
            while counter <= maxNumberOfPossibleAnswer:
                currentAnswer =  request.POST.getlist(f'ans_tf-{str(counter)}')
                if currentAnswer != []:
                    pass
                    if list_of_tf_question[questionindex].strip() == "":
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Question Before Submiting to For True False Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)


                    QuestionWithAns_tf[list_of_tf_question[questionindex]] = currentAnswer
                    
                    questionindex += 1
                else:
                    if len(removed_tf) > 0 and str(counter) not in removed_tf:
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Answer Before Submiting to For True False Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                    elif len(removed_tf) == 0:
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Answer Before Submiting to For True False Question'+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                        
                counter += 1

        if len(list_of_mp_question) >0 :

            if len(request.POST["counter_mp"])>0:
                maxNumberOfPossibleAnswer = int(request.POST["counter_mp"])
            else:
                maxNumberOfPossibleAnswer = 1
            removed = request.POST["removed_mp"] 
            
            counter = 1
            questionindex = 0

            while counter <= maxNumberOfPossibleAnswer:
                currentAnswer =  request.POST.getlist(f"ans_mp-{str(counter)}")
                if currentAnswer != []:
                    
                    currentInputChoices = str(counter)+"-"
                    currentInputChoices = request.POST.getlist(f"ch-{str(currentInputChoices) }")
                    ct = 1
                    for ans in currentInputChoices :
                        
                        if currentInputChoices[ct-1].strip() == "":
                            if ct == 1:
                                let = "A"
                            elif ct == 2:
                                let = "B"
                            elif ct == 3:
                                let = "C"
                            elif ct == 4:
                                let = "D"

                            messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Choices Before Submiting to For Multiple Choice Question '+ str(questionindex+1) + " Choice :"+let)
                            return redirect('exam_mgt_question_and_answer_inserting_page', course_id) 
                        
                            
                        ct += 1
                    if list_of_mp_question[questionindex].strip() == "":
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Question Before Submiting to For Multiple Choice Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                    
                    QuestionWithAns_mp[list_of_mp_question[questionindex]] = currentAnswer 
                    QuestionwithChoices_mp[list_of_mp_question[questionindex]]  = currentInputChoices
                    questionindex += 1   

                        
                else:
                    if len(removed) > 0 and str(counter) not in removed:
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Answer Before Submiting to For Multiple Choice Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                    elif len(removed) == 0:
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Answer Before Submiting to For Multiple Choice Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                        
                counter += 1  

        if len(list_of_fb_question) > 0:
            if len(request.POST["counter_fb"])>0:
                maxNumberOfPossibleAnswer = int(request.POST["counter_fb"])
            else:
                maxNumberOfPossibleAnswer = 1
            removed = request.POST["removed_fb"] 

            counter = 1
            questionindex = 0

            while counter <= maxNumberOfPossibleAnswer:
                currentAnswer =  request.POST.getlist(f"ans_fb-{str(counter)}") 
                
                if currentAnswer != [] and currentAnswer != [''] :
                    
                    if list_of_fb_question[questionindex].strip() == "":
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Question Before Submiting to For Fill in the blank Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                    
                    if "[ans]" not in list_of_fb_question[questionindex].strip():
                        messages.add_message(request, messages.ERROR, 'Make Sure u Inlcude [ans] signature in the question where dash should be placed in Fill in the blank questions'+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                        
                    
                    QuestionWithAns_fb[list_of_fb_question[questionindex]] = currentAnswer
                    questionindex += 1
                else:
                    if len(removed) > 0 and str(counter) not in removed:
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Answer Before Submiting to For    Fill in the blank Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
                    elif len(removed) == 0:
                        messages.add_message(request, messages.ERROR, 'Make Sure u Also Enter the appropirate Answer Before Submiting to For Fill in the blank Question '+ str(questionindex+1) )
                        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)       
                counter += 1

        random_number = random.randint(100000, 100000000000000)

        if len(QuestionWithAns_tf.values()) > 0:
            try:
                ExamSection = Examinationsection(
                                exam_tag = random_number,
                                type = "TF",
                                teacherid = current_employe_object,
                                courseinfn = Courseinformations.objects.get(course_id = course_id),
                       )
                
                ExamSection.save()
            except Exception as ww:
                print(ww)
                print("Xxxxxxxxxxxxxxxxxxxxx ERROR CODE 110 -------------Failed to save exam section of true false xxxxxxxxxxxxxxxxxx")
                return redirect('exam_mgt_question_and_answer_inserting_page', course_id)

            QuestionNumber = 1
            for quest , ans in QuestionWithAns_tf.items():
                try:
                    ExamContetn = ExaminationContent.objects.create(
                        questionid= ExamSection,
                        question = quest,
                        Answer = ans[0],
                        questionNumber = QuestionNumber,
                    )
                    ExamContetn.save()
                    
                except Exception as e:
                    print(e)
                    print("xxxxxxxxxxxxxxxxxxxxx Error code 111 Failed to save exam questions -----------xxxxxxxxxxxxxx")
                QuestionNumber += 1 
        else:
            messages.add_message(request, messages.ERROR, 'Make Sure U Also Enter the appropirate Question And Answer Before Submiting to For multiple choice Question '+ str(questionindex+1) )
            return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
        

        if len(QuestionWithAns_mp.values()) > 0:
            try:
                ExamSection = Examinationsection(
                                exam_tag = random_number,
                                type = "MC",
                                teacherid = current_employe_object,
                                courseinfn = Courseinformations.objects.get(course_id = course_id),
                             )
                ExamSection.save()
                pass
            except Exception as ww:
                print(ww)
                print("xxxxxxxxxxxxxx ERROR CODE 112 FAILED to exam store exam section for multiple choice section xxxxxxxxxxxxxxx")
            QuestionNumber = 1
            
            for quest , ans in QuestionWithAns_mp.items():
                
                try:
                    
                    ExamContetn = ExaminationContent.objects.create(
                        questionid= ExamSection,
                        question = quest,
                        questionNumber = QuestionNumber, 
                        Answer = ans[0],
                        Soultion1 = QuestionwithChoices_mp[quest][0],
                        Soultion2 = QuestionwithChoices_mp[quest][1],
                        Soultion3 = QuestionwithChoices_mp[quest][2],
                        Soultion4 = QuestionwithChoices_mp[quest][3],
                    )
                    ExamContetn.save()
                    
                except Exception as e:
                    print(e)
                    print("xxxxxxxxxxxxxxxxxxxxxx Error code 113 Failed to store multiple choice question and anser xxxxxxxxxxxx ")
                QuestionNumber += 1 
            
        else:
            messages.add_message(request, messages.ERROR, 'Make Sure U Also Enter the appropirate mltiple choice Question And Answer Before Submiting to For Question '+ str(questionindex+1) )
            return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
        

        if len(QuestionWithAns_fb.values()) > 0:
            try:
                ExamSection = Examinationsection(
                                exam_tag = random_number,
                                type = "FB",
                                teacherid = current_employe_object,
                                courseinfn = Courseinformations.objects.get(course_id = course_id),
                            )
                ExamSection.save()
            except Exception as ww:
                print(ww)
                print("xxxxxxxxxxxxxxxxxxxxxx FAILED TO STORE SECTION FOR FILL IN THE BLANK QUESTION ERROR CODE 114 xxxxxxxxxxxxxxxxxxxxxxx")
            
            
            QuestionNumber = 1
            for quest , ans in QuestionWithAns_fb.items():
                
                try:
                    ExamContetn = ExaminationContent.objects.create(
                        questionid= ExamSection,
                        question = quest,
                        Answer = ans[0],
                        questionNumber = QuestionNumber,
                    )
                    ExamContetn.save()
                    
                except Exception as e:
                    print(e)
                    print("xxxxxxxxxxxxxxxxxxxxx FAILED TO STORE EXAM CONTENT FOR Error code 116 FOR FILL IN THE BLANK teacher XXXXXXXXXXXXXXXXXXXXXXX")
                QuestionNumber += 1 
            
        else:
            messages.add_message(request, messages.ERROR, 'Make Sure U Also Enter the appropirate Question fill in the blank And Answer Before Submiting to For Question '+ str(questionindex+1) )
            return redirect('exam_mgt_question_and_answer_inserting_page', course_id)


        messages.add_message(request, messages.SUCCESS, 'Examination Uploaded Sucessfully!' )
        return redirect('exam_mgt_question_and_answer_inserting_page', course_id)
    

    context = {
        'course_id':course_id,
    }
    return render(request, 'Teacher/examination_question_and_answer_inserting_page.html', context= context)
    
@login_required(login_url='base_login_page')
@school_teacher_only
def exam_management_detail_view_page(request, course_id, examsection_id):
    
    exams_list = ExaminationContent.objects.filter(questionid = Examinationsection.objects.get(id = examsection_id))

    tf_list = []
    mc_list = []
    fb_list = []
    for exam in exams_list:
        if exam.questionid.type == 'TF':
            tf_list.append(exam)
        elif exam.questionid.type == 'MC':
            mc_list.append(exam)
        elif exam.questionid.type == 'FB':
            fb_list.append(exam)

    
    context = {
        'course_id':course_id,
        'examsection_id':examsection_id,
        
        'tf_list':tf_list,
        'is_tf_empty':len(tf_list) > 0,
        
        'mc_list':mc_list,
        'is_mc_empty':len(mc_list)>0,

        'fb_list':fb_list,
        'is_fb_empty':len(fb_list)>0
    }
    return render(request, 'Teacher/examination_information_detail_view_page.html', context = context)




@login_required(login_url='base_login_page')
@school_teacher_only
def assignment_mgt_course_list_view_page(request):
    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)

    availabel_course_list = TeacherToCourseMapping.objects.filter(teacher = current_employe_object)
    
    availabel_list_courses_list_final = []

    for map in availabel_course_list:
        [availabel_list_courses_list_final.append(course) for course in map.course_info.all()]
    
    context = {
        'course_list':availabel_list_courses_list_final,
        'is_empty':len(availabel_list_courses_list_final) > 0
    }
    return render(request, 'Teacher/assignment_mgt_page.html' , context = context)


@login_required(login_url='base_login_page')
@school_teacher_only
def assignment_mgt_course_specific_list_view_page(request, course_id):

    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)
    
    courseinfn = Courseinformations.objects.get(course_id = course_id )
    assignement = AssignmentContent.objects.filter(Q(courseinfn = courseinfn) & Q(teacherid = current_employe_object))

    
    context = {
        'course_id':course_id,
        'assignements':assignement,
        'is_assignment_empty':len(assignement) > 0
    }
    return render(request, 'Teacher/assignment_mgt_course_specific_mgt_page.html', context = context)

@login_required(login_url='base_login_page')
@school_teacher_only
def assignment_mgt_assignment_uploding_page(request, course_id):

    if request.method == "POST":
        
        listOfPDFTypes = ['.DOC', '.DOCX', '.ODT','.PDF', '.XLSX', '.XLS', '.ODS', '.PPT','.PPTX','.TXT' ]
 
        file = request.FILES['assignment_file']
        extesionpdf   =  os.path.splitext(str(request.FILES['assignment_file']))
        
        if fileTypeChecker(extesionpdf[1], listOfPDFTypes ):
            pass
        else:
            print("Document Mismatch")
            # display error message tells user to change the file typeuse for pdf file
            return redirect('assignment_mgt_assignment_uploding_page', course_id )
        user_object = User.objects.get(username=request.user)
        current_employe_object = Employee.objects.get(userObject = user_object)
        
        try:
            AssignmentContent.objects.create(
                pdf = file,
                teacherid = current_employe_object,
                courseinfn = Courseinformations.objects.get(course_id = course_id )
            )
            print('xxxxxxxxxxxxxxxxxxxxxxxx Successfully registered Assignment information xxxxxxxxxxxxxxxxxxxxxxx ')

            return redirect('assignment_mgt_course_specific_list_view_page', course_id)
        except:
            print("xxxxxxxxxxxxxxxxxxxxxx Failed to registred Assignement information xxxxxxxxxxxxxxxxxxxxxxxxxx")

            return redirect('assignment_mgt_assignment_uploding_page', course_id)
    
    return render(request,'Teacher/assignment_content_uploading_page.html')

@login_required(login_url='base_login_page')
@school_teacher_only
def assignment_content_detail_view_page(request, course_id, assignment_id):


    ass_content = AssignmentContent.objects.get(id = assignment_id)
    context = {
        'course_id':course_id,
        'assignment_id':assignment_id,
        'ass_content':ass_content
    }
    return render(request, 'Teacher/assignment_content_detail_view_page.html', context)

@login_required(login_url='base_login_page')
@school_teacher_only
def assignment_submmited_management_page(request, course_id):

    user_object = User.objects.get(username=request.user)
    current_employe_object = Employee.objects.get(userObject = user_object)
        
    assignement_interaction_student = AssignmentStudentInteraction.objects.all()

    assignment_for_current_teacher = []
    for studnet_intex in assignement_interaction_student:
        if studnet_intex.assignment.teacherid.employeeid == current_employe_object.employeeid:
            assignment_for_current_teacher.append(studnet_intex)
    
    context = {
        'list_of_submmited_assignements' : assignment_for_current_teacher,
        'is_there_new_submission':len(assignment_for_current_teacher) > 0,
        'course_id':course_id
    }
    return render(request, 'Teacher/assignment_submmited_management_page.html', context= context)


@login_required(login_url='base_login_page')
@school_teacher_only
def assignement_submitted_detail_view_page(request, course_id, intx_id):
    course_intx = AssignmentStudentInteraction.objects.get(id = intx_id)

    if request.method == "POST":
        tottal_mark = request.POST['tottal_mark']
        result = request.POST['result']
        try:
            AssignmentAssesment.objects.create(
                stduentid = course_intx.stduentid,
                assignment_id = course_intx.assignment,
                tottalMark = tottal_mark,
                result = result,
                std_intx = course_intx
            )
            print("xxxxxxxxxxxx 117 successfully inserted result for assignment xxxxxxxxxxxxxxxxxxxxxxx")
            return redirect('assignment_submmited_management_page',course_id )
        except:  
            print("xxxxxxxxxxxxxxxxxxxxxxxxx Filed 116 to sore result for student assignement xxxxxxxxxxxxxxxx")
            return redirect('assignement_submitted_detail_view_page',course_id, intx_id )
    
    context = {
        'course_id':course_id,
        'intx_id':intx_id,
        "interaction":course_intx, 
    }

    try:
        assesment = AssignmentAssesment.objects.get(stduentid = course_intx.stduentid, assignment_id= course_intx.assignment, std_intx = course_intx)
        context['is_marked']  = True
        context["marks"] = assesment
    except:
        context['is_marked']  = False

    return render(request, "Teacher/assignment_submitted_detail_view_page.html", context=context)



