from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators  import *
# Create your views here.


def school_admin_landingpage(request):
    return render(request, "School_Admin/index.html")


def login_page(request):
    if request.method == 'POST':
        user_name = request.POST['username'].strip()
        password =  request.POST['password'].strip()
        
        user = authenticate(request, username=user_name,  password=password)

        if user is not None :
            login(request, user)
            if request.user.is_authenticated :
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                    if str(group).strip().lower == 'School_Manager'.lower:
                        #do ur thing
                        pass
                    print("---------we mtached to the dashboard")
                    
                logout(request)
                return redirect('landing_page_school_admin')
        else:
            print("i don't have group")

    return render(request, 'School_Admin/login.html')

