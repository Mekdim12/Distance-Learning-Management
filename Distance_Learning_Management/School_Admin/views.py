from django.shortcuts import render

# Create your views here.


def school_admin_logingpage(request):
    return render(request, "School_Admin/index.html")


def login_page(request):
    if request.method == 'POST':
        userName = request.POST.get('username')
        password =  request.POST.get('password')
        
    return render(request, 'School_Admin/login.html')

