from django.shortcuts import redirect
from django.contrib.auth.models import User
from School_Admin.models import *

def shoold_doh_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Teacher':
            user_object = User.objects.get(username=request.user)
            current_employe_object = Employee.objects.get(userObject = user_object)
                        
            if Department.objects.filter(departement_head = current_employe_object).exists():
                return view_func(request,*args,**kwargs)
            else:
                return redirect('base_login_page')

        else:
            return redirect('base_login_page')

    return wrapper_function