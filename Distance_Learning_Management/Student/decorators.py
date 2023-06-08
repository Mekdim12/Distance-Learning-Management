from django.shortcuts import redirect
from django.contrib.auth.models import User
from School_Admin.models import *

def school_student_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Student':
            return view_func(request,*args,**kwargs) 
        else:
            return redirect('base_login_page')

    return wrapper_function
