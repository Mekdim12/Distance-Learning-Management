from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from School_Admin.models import Employee

class Command(BaseCommand):
  
    def handle(self, *args, **kwargs):
        # removing the user name from main model cusz its in Unser onejct
        
        userObject = User.objects.create_user(username = 'mekdimtam', email= 'mekdimtamiratcoder@gmail.com', password = 'mekdimtam')
        userObject.first_name = 'Mekdim'
        userObject.last_name = 'Tamirat'
        userObject.save()

        admin_emply = Employee(
                 firstname = 'Mekdim',
                middlename= 'Tamirat',
                lastname="hailu",
                gender = 'M',
                phonenumber = '0924041650',
                address = "Addis ababa",
                email="mekdimtamiratcoder@gmail.com",
                employeeid='AD00001', 
                userObject =  userObject  
        )

        try:
            my_group = Group.objects.get_or_create(name='School_Manager') 
            my_group = Group.objects.get(name='School_Manager')
            # my_group.user_set.add(userObject)
            userObject.groups.add(my_group) 

            admin_emply.save()
        except Exception as e:
            print(e)
            print("xxx Failed to initalize the system xxx")
            return
        

        print("--------------- system setup with access for admin is done -------------")
       