from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''
jobtype
compnayname
industry
preffered lanaguage


'''
class StudentInformation(models.Model):
    userid = models.CharField(db_column='UserId', primary_key=True, max_length=104)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=100)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=100)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=100)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=100)  # Field name made lowercase.
    woredazone = models.CharField(db_column='WoredaZone', max_length=100)  # Field name made lowercase.
    streetkebele = models.CharField(db_column='StreetKebele', max_length=100)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profilePicture = models.ImageField (db_column='profilePicture', upload_to='Images/')
    student_cv_pdf_file = models.FileField(upload_to='Files/')
    email = models.EmailField(max_length=55, null=True)   
    is_photos_taken = models.BooleanField(default=False)
    userObject = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'StudentInformation'
       