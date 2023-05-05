from django.urls import path, include
from .views import school_admin_logingpage

urlpatterns = [
    path('', school_admin_logingpage, name="login_page_school_admin"),
   
]
