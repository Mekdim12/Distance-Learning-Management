from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from School_Admin.models import Employee

class Command(BaseCommand):
  
    def handle(self, *args, **kwargs):
        # removing the user name from main model cusz its in Unser onejct
        
        userObject = User.objects.create_user(username = 'doh-admin', email= 'doh@gmail.com', password = 'doh')
        userObject.first_name = 'doh'
        userObject.last_name = 'project'
        userObject.save()

        admin_emply = Employee(
                 firstname = 'Doh',
                middlename= 'Project',
                lastname="Admin",
                gender = 'M',
                phonenumber = '999999999',
                address = "Debretabor",
                email="doh@gmail.com",
                employeeid='AD00001', 
                userObject =  userObject  
        )

        try:
            my_group = Group.objects.get_or_create(name='School_Manager') 
            Group.objects.get_or_create(name='Registerar') 
            Group.objects.get_or_create(name='Teacher') 
            Group.objects.get_or_create(name='Student')
            # Group.objects.get_or_create(name='DOH')  
            
            
            my_group = Group.objects.get(name='School_Manager')
            userObject.groups.add(my_group) 

            admin_emply.save()
        except Exception as e:
            print(e)
            print("xxx Failed to initalize the system xxx")
            return
        

        print("xxxxxxxxxxxxxxxxxx system setup with access for admin is done xxxxxxxxxxxxxxxxxxxx")
       