from django.shortcuts import redirect


def school_manager_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'School_Manager':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('admin_main_landing_page')

    return wrapper_function