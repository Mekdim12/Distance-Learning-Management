from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

CHOICE2 = [
        ('Male','Male'),
        ('Female', 'Female')
    ]
ROLE = [
    ('Teacher', 'Teacher'),
    ('Registrar', 'Registrar'),
     ('Admin', 'Admin'),

]
PROGRAMS = [
     ('Bachelor degree', 'Bachelor Degree'),
     ('Master Degree', 'Master Degree'),
]


class Employee(models.Model):
    firstname = models.CharField(db_column='FirstName', max_length=140)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=104)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=104)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=104, default="")  # Field name made lowercase.
    gender = models.CharField(db_column='Gender',choices=CHOICE2, max_length=6, default="private")  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=103)  # Field name made lowercase.
    address = models.CharField(db_column='Country',max_length=104)
    email = models.EmailField(max_length=55, null=True)
    employeeid = models.CharField(db_column='EmployeeID', primary_key=True, max_length=104)  # Field name made lowercase.
    userObject = models.OneToOneField(User, on_delete=models.CASCADE,) 
    class Meta:
        db_table = 'employee'
    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
class RoleInSchool(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employee_role = models.CharField(choices=ROLE, max_length=150)

    def __str__(self):

         return f'{self.employee.firstname} {self.employee.lastname}'
    

class Faculty(models.Model):
    facult_adminstrator = models.OneToOneField(Employee, models.DO_NOTHING)
    full_faculty_name = models.CharField(max_length = 500)

    def __str__(self) -> str:
        return self.full_faculty_name
  
class Department(models.Model):
    name_of_department = models.CharField(max_length=250)
    faculty_info = models.ForeignKey(Faculty, models.DO_NOTHING)
    departement_head = models.OneToOneField(Employee, models.DO_NOTHING)
    
    def __str__(self) -> str:
        return self.name_of_department
    


# -------------------- main course and realated models start ------------------------

class Courseinformations(models.Model):
    course_id = models.CharField(db_column='Course_ID', primary_key=True, max_length=104)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_Name', max_length=200,  null=True)  # Field name made lowercase.
    level_of_difficulties = models.IntegerField( null=True)
    objectiveOfCourse = models.CharField(db_column='CourseObjective', max_length=200 , null=True) 
    lanaguage = models.CharField(db_column='Language', max_length= 200, null=True)  # Field name made lowercase.
    tottal_credit_hour = models.IntegerField()
    departement = models.ForeignKey(Department, models.DO_NOTHING, null=True)
    programs = models.CharField(max_length=100,choices=PROGRAMS)

    class Meta:
        db_table = 'courseinformations'

    def __str__(self):
        return str(self.course_name)

class tableofContentOfMainCourseInformation(models.Model):
    courseid = models.ForeignKey(Courseinformations, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    topic = models.CharField(max_length=150, null=True)
    class Meta:
        db_table = "tableOfContentofCourseInformation"
        unique_together = (('courseid',  'topic'),)


class MainCoursecontent(models.Model):
    courseid = models.ForeignKey(Courseinformations, models.DO_NOTHING, db_column='MaincourseId')  # Field name made lowercase.
    tableofcontent = models.ForeignKey( tableofContentOfMainCourseInformation , models.DO_NOTHING, db_column='tableOFContent', blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = 'Maincoursecontent'
        unique_together = (('courseid', 'tableofcontent'),)

class MainCoursecontentdetailcontent(models.Model):
    courseid = models.ForeignKey(Courseinformations, models.DO_NOTHING, db_column='courseId')  # Field name made lowercase.
    pdf   = models.FileField(upload_to='Files/MainCourseAsset',db_column="PDF" )
    audio = models.FileField(upload_to='Files/MainCourseAsset',db_column="Audio")
    video = models.FileField(upload_to='Files/MainCourseAsset',db_column= "Video")
    notes = RichTextUploadingField(blank = True, null = True, db_column="Notes")
    topic = models.CharField(max_length=150, null=True)
    course_creator = models.ForeignKey(Employee, models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'Maincoursecontentdetailcontent'


class PriceForDepartements(models.Model):
    department = models.OneToOneField(Department, on_delete=models.DO_NOTHING)
    price = models.FloatField()
    