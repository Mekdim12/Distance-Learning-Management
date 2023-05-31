from django.db import models
from School_Admin.models import *
# Create your models here.

class TeacherToCourseMapping(models.Model):
    course_info = models.ManyToManyField(Courseinformations)
    teacher = models.ForeignKey(Employee, models.DO_NOTHING)

    