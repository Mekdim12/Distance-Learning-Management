from django.db import models

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
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=100)  # Field name made lowercase.
    woredazone = models.CharField(db_column='WoredaZone', max_length=100)  # Field name made lowercase.
    streetkebele = models.CharField(db_column='StreetKebele', max_length=100)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profilePicture = models.ImageField (db_column='profilePicture', upload_to='Images/')
    disability = models.CharField(max_length=132,  null=True)
    jobtype = models.CharField(max_length=132,  null=True)
    student_cv_pdf_file = models.FileField(upload_to='Files/')
    email = models.EmailField(max_length=55, null=True)   
    is_photos_taken = models.BooleanField(default=False)

    class Meta:
        db_table = 'StudentInformation'
        unique_together = (('firstname', 'userid', 'middlename', 'lastname'),)
