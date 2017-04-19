from django import forms
from .models import UserFilters


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    student_id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
# email = forms.EmailField(required=False)


class FilterForm(forms.ModelForm):
    # Time fiters
    class Meta:
        model = UserFilters
        exclude = ['user']


class DPRUploadForm(forms.Form):
    docfile = forms.FileField(
        label='Select you DPR file',
        help_text='but don\'t tell anyone'
    )
