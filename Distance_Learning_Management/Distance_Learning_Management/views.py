from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


import random

# Create your views here.

def landing_page(request):
    return render(request, 'index.html')

def login_page(request):
    if request.user.is_authenticated: # if alrady logged in
        group = request.user.groups.all()[0].name
        if str(group).strip().lower() == 'School_Manager'.lower():
            return redirect('admin_main_landing_page')
        

    if request.method == 'POST':
        user_name = request.POST['username'].strip()
        password =  request.POST['password'].strip()
        user = authenticate(request, username=user_name,  password=password)

        if user is not None :
            login(request, user)
            if request.user.is_authenticated :
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                    if str(group).strip().lower() == 'School_Manager'.lower():
                        return redirect('admin_main_landing_page')
                   
                                      
                logout(request)
                return redirect('base_login_page')
        else:
            return redirect('base_login_page')
            
    return render(request, 'base_login.html')
