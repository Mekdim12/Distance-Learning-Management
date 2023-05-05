from django.shortcuts import render

# Create your views here.


def school_admin_logingpage(request):
    return render(request, "School_Admin/index.html")