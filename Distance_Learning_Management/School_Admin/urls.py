from django.urls import path, include
from .views import school_admin_logingpage,login_page

urlpatterns = [
    path('', school_admin_logingpage, name="login_page_school_admin"),
    path('login',login_page, name="admin_login_page")
   
]
