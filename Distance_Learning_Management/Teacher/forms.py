from django import forms
from django.forms import ModelForm,widgets
from School_Admin.models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget 

class MainCoursecontentdetailcontentForm(forms.ModelForm):
    class Meta:
        model = MainCoursecontentdetailcontent
        fields = '__all__'
        widgets = {
            "pdf":forms.ClearableFileInput(attrs = {'class':'form-control ', 'name':'pdf'}),
            "audio":forms.ClearableFileInput(attrs = {'class':'form-control ', 'name':'audio'}),
            "video":forms.ClearableFileInput(attrs = {'class':'form-control ', 'name':'video'}),
            "topic":forms.TextInput(attrs = {'class':'form-control ','name':'topic' }),
            "notes":CKEditorUploadingWidget(attrs = {'class':'form-control ', 'name':'notes'})
        }
