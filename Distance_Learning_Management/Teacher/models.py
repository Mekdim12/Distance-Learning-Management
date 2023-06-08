from django.db import models
from Doh.models import *
from School_Admin.models import *
from Reception.models import *

from datetime import date

# Create your models here.

#-----------------------------------------------------------------------------------------


class Examinationsection(models.Model):
    type = models.CharField(max_length=150, blank=True, db_column="TypeOfQuestion")
    date = models.DateField(default = date.today, db_column="Date", blank=True, null=True)
    teacherid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='teacherId')  # Field name made lowercase.
    courseinfn = models.ForeignKey(Courseinformations,models.DO_NOTHING, db_column='courseInformationId', blank=True)  # Field name made lowercase.
    class Meta:
        db_table = 'Examinationsection'
        

class Assesments(models.Model):
    stduentid = models.ForeignKey(StudentInformation, models.DO_NOTHING, db_column='StduentID')  # Field name made lowercase.
    questionid = models.ForeignKey(Examinationsection, models.DO_NOTHING,db_column='QuestionId')  # Field name made lowercase.
    tottalMark = models.IntegerField(db_column='Tottal_Mark')  # Field name made lowercase.
    result = models.FloatField(db_column='Result')  # Field name made lowercase.
    date = models.DateField(default = date.today, db_column="Date", blank=True, null=True)
    listofCorrectEntries = models.CharField(blank=True,max_length=30000, null=True ,db_column="Correctly_Answered")
    listofInCorrectEntries = models.CharField(blank=True,max_length=30000, null=True ,db_column="InCorrectly_Answered")
    listOfTrial = models.IntegerField(db_column='NumberOfTrials' , default=0)
    class Meta:
        db_table = 'Assesments'


class ExaminationContent(models.Model):
    questionid = models.ForeignKey(Examinationsection, models.DO_NOTHING, db_column='QuestionIds')
    questionNumber = models.IntegerField(db_column ="QuestionNumber" ,default= 0)
    question = models.TextField(blank=True,db_column="Question")
    Answer = models.TextField(blank=True,db_column="Answer")
    Soultion1 = models.CharField(blank=True, max_length=30000,db_column="Solution1",null=True)
    Soultion2 = models.CharField(blank=True, max_length=30000,db_column="Solution2",null=True)
    Soultion3 = models.CharField(blank=True, max_length=30000,db_column="Solution3",null=True)
    Soultion4 = models.CharField(blank=True, max_length=30000,db_column="Solution4",null=True)

    class Meta:
        db_table = 'ExaminationContent'


class StudentEngageExaminationSection(models.Model):
    studentid = models.ForeignKey(StudentInformation, models.DO_NOTHING, db_column='studentID', blank=True, null=True)  # Field name made lowercase.
    questionid = models.ForeignKey(Examinationsection, models.DO_NOTHING, db_column='questionId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'StudentEngageExaminationSection'

class AssignmentContent(models.Model):
    pdf   = models.FileField(upload_to='Files/Assignments',db_column="PDF" )
    date = models.DateField(default = date.today, db_column="Date", blank=True, null=True)
    teacherid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='teacherId')  # Field name made lowercase.
    courseinfn = models.ForeignKey(Courseinformations,models.DO_NOTHING, db_column='courseInformationId', blank=True)  # Field name made lowercase.
class AssignmentStudentInteraction(models.Model):
    stduentid = models.ForeignKey(StudentInformation, models.DO_NOTHING, db_column='StduentID')  # Field name made lowercase.
    assignment = models.ForeignKey(AssignmentContent, models.DO_NOTHING)
    is_submitted = models.BooleanField(default=False)
    submitted   = models.FileField(upload_to='Files/submittedAssignments',db_column="PDF" )


class AssignmentAssesment(models.Model):
    stduentid = models.ForeignKey(StudentInformation, models.DO_NOTHING, db_column='StduentID')  # Field name made lowercase.
    assignment_id = models.ForeignKey(AssignmentContent, models.DO_NOTHING,db_column='AssignmentsID')  # Field name made lowercase.
    tottalMark = models.IntegerField(db_column='Tottal_Mark')  # Field name made lowercase.
    result = models.FloatField(db_column='Result')  # Field name made lowercase.
    date = models.DateField(default = date.today, db_column="Date", blank=True, null=True)
    std_intx = models.ForeignKey(AssignmentStudentInteraction, models.DO_NOTHING, null=True, blank=True)









