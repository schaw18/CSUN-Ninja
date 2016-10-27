from django import forms
from .models import UserFilters

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)

class FilterForm(forms.ModelForm):
    # Time fiters
    class Meta:
        model = UserFilters
        exclude =['user']