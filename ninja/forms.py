from django import forms
from .models import UserFilters

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    

class FilterForm(forms.ModelForm):
    # Time fiters
    class Meta:
        model = UserFilters
        exclude =['user']

class DPRUploadForm(forms.Form):
    docfile = forms.FileField(
        label='Select you DPR file',
        help_text='but don\'t tell anyone'
    )