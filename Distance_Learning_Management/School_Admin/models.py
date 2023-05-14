from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CHOICE2 = [
        ('Male','Male'),
        ('Female', 'Female')
    ]
ROLE = [
    ('Teacher', 'Teacher'),

]

class Employee(models.Model):
    firstname = models.CharField(db_column='FirstName', max_length=140)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=104)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=104)  # Field name made lowercase.
    teacher_info = models.CharField(db_column='UserName', max_length=104, default="")  # Field name made lowercase.
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
    