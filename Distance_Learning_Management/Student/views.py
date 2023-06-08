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
from django.contrib import messages
import random
import os
# Create your views here.


@login_required(login_url='base_login_page')
@school_student_only
def homepage_for_student(request):
    return render(request, "Student/index.html")