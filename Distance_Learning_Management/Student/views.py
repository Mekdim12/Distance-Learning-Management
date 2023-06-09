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

import threading


import glob
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner
import time
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np
from django.contrib.auth.decorators import login_required
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import datetime
import seaborn as sns
import pandas as pd
from django.db.models import Count
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from matplotlib import rcParams
import math

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

@login_required(login_url='base_login_page')
@school_student_only
def student_exam_list_view_page(request):
    
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)

    student_acadmaic_option = StudentAcademicOption.objects.get(student_id = current_std_object)
    
    course_list = Courseinformations.objects.filter(departement =student_acadmaic_option.departement,  programs =student_acadmaic_option.programs)

    list_of_exams_registered = []
    for course in course_list:       
        [list_of_exams_registered.append(exams) for exams in   Examinationsection.objects.filter(courseinfn = course)]

    final_list_of_exams = []
    for exam in list_of_exams_registered:
        list_assesments = Assesments.objects.filter(stduentid = current_std_object, questionid = exam)
        [final_list_of_exams.append(assesment) for assesment in list_assesments ]

    
    context = {
        "final_list_of_exams":final_list_of_exams,
        "is_empty":len(final_list_of_exams)
    }
    return render(request, "Student/examination_list_view_page.html", context = context)


@login_required(login_url='base_login_page')
@school_student_only
def student_exam_list_view_for_newer_exams(request):
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)

    student_acadmaic_option = StudentAcademicOption.objects.get(student_id = current_std_object)
    
    course_list = Courseinformations.objects.filter(departement =student_acadmaic_option.departement,  programs =student_acadmaic_option.programs)

    list_of_exams_registered = []
    for course in course_list:       
        [list_of_exams_registered.append(exams) for exams in   Examinationsection.objects.filter(courseinfn = course)]
    
    list_of_exams = []
    for exam in list_of_exams_registered:
        list_assesments = Assesments.objects.filter(stduentid = current_std_object, questionid = exam)
        [list_of_exams.append(assesment) for assesment in list_assesments ]

    
    final_list_of_exams = []
    for exam in list_of_exams_registered:
        list_assesments = Assesments.objects.filter(stduentid = current_std_object, questionid = exam)
        if len(list_assesments) > 0:
            for assesment in list_assesments:
                if assesment not in list_of_exams:
                    final_list_of_exams.append(exam)
        else:
            final_list_of_exams.append(exam)


    list_of_tags = []
    for assesment in final_list_of_exams:
        if assesment.exam_tag not in list_of_tags:
            list_of_tags.append(assesment.exam_tag)
    
    tag_to_counter = {}
    for tag in list_of_tags:
        exam_sections = Examinationsection.objects.filter(exam_tag=tag)
        count_TF = 0
        count_MC = 0
        count_FB = 0
        for exam_section in exam_sections:
            if exam_section.type == "TF":
                count_TF +=1
            elif exam_section.type == "MC":
                count_MC += 1
            elif exam_section.type == "FB":
                count_FB += 1

        tag_to_counter[exam_sections[0]] = [count_TF, count_MC, count_FB]
    
    context = {
        "new_exams":tag_to_counter,
        "is_empty":len(tag_to_counter)>0,  
    }

    return render(request, "Student/examination_taking_page_list_view_page.html", context = context)


class background_running_thread(threading.Thread):
    def __init__(self, studentid):
        self.studentid = studentid
        self.time = time.time()
        threading.Thread.__init__(self)

    def predict(self, face_aligned,svc,threshold=0.7):
        face_encodings=np.zeros((1,128))
        try:
            x_face_locations=face_recognition.face_locations(face_aligned)
            faces_encodings=face_recognition.face_encodings(face_aligned,known_face_locations=x_face_locations)
            if(len(faces_encodings)==0):
                return ([-1],[0])

        except:

            return ([-1],[0])

        prob=svc.predict_proba(faces_encodings)
        result=np.where(prob[0]==np.amax(prob[0]))
        try:
            if(prob[0][result[0]]<=threshold):
                return ([-1],prob[0][result[0]])
        except:
            pass

        return (result[0],prob[0][result[0]])

    def check_student_is_real_one(self, studentid):
        
        
        try:
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('face_recognition_data/shape_predictor_68_face_landmarks.dat')
            svc_save_path="face_recognition_data/svc.sav"
            flagFaceMatched =  0
            with open(svc_save_path, 'rb') as f:
                svc = pickle.load(f)
            
            fa = FaceAligner(predictor , desiredFaceWidth = 96)
            encoder=LabelEncoder()
            encoder.classes_ = np.load('face_recognition_data/classes.npy')
            
            faces_encodings = np.zeros((1,128))
            no_of_faces = len(svc.predict_proba(faces_encodings)[0])
            count = dict()
            present = dict()
            log_time = dict()
            start = dict()
            for i in range(no_of_faces):
                count[encoder.inverse_transform([i])[0]] = 0
                present[encoder.inverse_transform([i])[0]] = False
            vs = VideoStream(src=0).start()
            
            sampleNum = 0
            flag = True
            while(flag):
                frame = vs.read()
            
                try:
                    frame = imutils.resize(frame ,width = 800)
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = detector(gray_frame,0)
                    
                except:
                    flagFaceMatched = False
                    flag = False
                for face in faces:
                    # print("INFO : inside for loop")
                    (x,y,w,h) = face_utils.rect_to_bb(face)
                    face_aligned = fa.align(frame,gray_frame,face)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
                    (pred,prob)=self.predict(face_aligned,svc)
                    try:
                        

                        if(pred!=[-1]):
                            person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                            pred=person_name
                            if count[pred] == 0:
                                if self.time is None:
                                    self.time  = time.time()
                                

                                start[pred] = time.time()
                                count[pred] = count.get(pred,0) + 1
                            if count[pred] == 4 and (time.time()-start[pred]) > 1.2:
                                count[pred] = 0
                            else:
                                present[pred] = True
                                log_time[pred] = datetime.datetime.now()
                                count[pred] = count.get(pred,0) + 1
                                self.time = time.time()
                                if count[pred] == 4:
                                    flagFaceMatched  = True
                                    if pred == studentid:
                                        flag = False
                                        flagFaceMatched = True
                                    
                            cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
                        else:
                            ct = time.time()

                            if ct-self.time > 25:
                                flag = False
                                break
                            person_name="unknown"
                            flagFaceMatched = False
                            cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
                            
                    except:
                        ct = time.time()
                        if ct-self.time > 25:
                            flag = False

                            break
                        person_name="unknown"
                        flagFaceMatched = False
                        cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
                        break
                
                cv2.imshow("Face Recognition make sure ur face is visible",frame)
                key=cv2.waitKey(50) & 0xFF
                
            vs.stop()
            # vid.release()
            cv2.destroyAllWindows()
        except Exception:
            return redirect('student_exam_list_view_for_newer_exams')

        if not flagFaceMatched:
            return redirect('student_exam_list_view_for_newer_exams')
    
    def run(self):
        self.check_student_is_real_one(self.studentid)


@login_required(login_url='base_login_page')
@school_student_only
def examination_student_taking_page(request, tag_id):

    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)


    tf_questions = Examinationsection.objects.filter(exam_tag = tag_id, type = "TF")
    mc_questions = Examinationsection.objects.filter(exam_tag = tag_id, type = "MC")
    fb_questions = Examinationsection.objects.filter(exam_tag = tag_id, type = "FB")

    tf_content = []
    for tf_quest in tf_questions:
        tf_question_content = ExaminationContent.objects.filter(questionid = tf_quest)
        [tf_content.append(question) for question in tf_question_content]

    mc_content = []
    for mc_quest in mc_questions:
        mc_question_content = ExaminationContent.objects.filter(questionid = mc_quest)
        [mc_content.append(question) for question in mc_question_content]
    
    fb_content = []
    for fb_quest in fb_questions:
        fb_question_content = ExaminationContent.objects.filter(questionid = fb_quest)
        [fb_content.append(question) for question in fb_question_content]
    
    if request.method == "POST":

        ExamObjectt = Examinationsection.objects.filter(exam_tag = tag_id) 
        
        listOfCorrectAnswersNumber = 0
        listofInCorrectAnswersNumber = 0

        keys = request.POST.keys()
        for i in list(keys):

            if str(i).startswith("MC-"):
                mc = request.POST[i]
                splitted = str(i).split('-')
                question_number = splitted[1]
                id = splitted[2]
                ExamsContetns = ExaminationContent.objects.get(id = id, questionNumber= int(question_number) )
                
                if ExamsContetns.Answer == mc:
                    listOfCorrectAnswersNumber += 1
                else:
                    listofInCorrectAnswersNumber += 1

            elif str(i).startswith("TF-"):
                tf = request.POST[i]
                splitted = str(i).split('-')
                question_number = splitted[1]
                id_ = splitted[2]
                ExamsContetns = ExaminationContent.objects.get(id = id_, questionNumber= int(question_number) )
                
                if ExamsContetns.Answer == tf:
                    listOfCorrectAnswersNumber += 1
                else:
                    listofInCorrectAnswersNumber += 1

            elif str(i).startswith("FB-"):
                fb = request.POST[i]
                splitted = str(i).split('-')
                question_number = splitted[1]
                idfb = splitted[2]
                ExamsContetns = ExaminationContent.objects.get(id = idfb, questionNumber= int(question_number) )
                
                if ExamsContetns.Answer == fb:
                    listOfCorrectAnswersNumber += 1
                else:
                    listofInCorrectAnswersNumber += 1
        

        try:
            asses = Assesments.objects.create(
                    stduentid = current_std_object,
                    questionid = ExamObjectt[0],
                    tottalMark = listOfCorrectAnswersNumber+listofInCorrectAnswersNumber,
                    result = listOfCorrectAnswersNumber,
                    listofCorrectEntries = listOfCorrectAnswersNumber,
                    listofInCorrectEntries = listofInCorrectAnswersNumber,
                    listOfTrial = 1
                )
            return redirect('exam_result',asses.id )
        except Exception as e:
            print(e)
            print("xxxxxxxxxxxxx 150 Failed to store Exam Result xxxxxxxxxxxxxxx")
            return redirect('student_exam_list_view_for_newer_exams')
                
    user_object = User.objects.get(username=request.user)
    current_std_object = StudentInformation.objects.get(userObject = user_object)


    tf_questions = Examinationsection.objects.filter(exam_tag = tag_id, type = "TF")
    mc_questions = Examinationsection.objects.filter(exam_tag = tag_id, type = "MC")
    fb_questions = Examinationsection.objects.filter(exam_tag = tag_id, type = "FB")
    
    

    content = {}
    for exam in fb_content:
        
        replaceText = exam.question
        replaceText = replaceText.replace("[ans]", " __________________________ ")
        content[exam] = replaceText

    context = {
        "tf":tf_content,
        "mc":mc_content,
        "fb_content":fb_content,
        "content":content
    }
    background_running_thread(current_std_object).start()
    return render(request, "Student/examination_exam_taking_page.html", context = context)


@login_required(login_url='base_login_page')
@school_student_only
def exam_result_showing_page(request, asses_id):

    assesment = Assesments.objects.get(id = asses_id)

    context = {
        "assement":assesment,
        
    }
    return render(request, "Student/exam_result_showing_page.html", context= context)
    

