from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from .models import *


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])

            if user is not None:

                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Authorization successful.')

                else:
                    messages.add_message(request, messages.INFO, 'This user is suspended')
                    return render(request, 'ninja/login.html', {'form': form})
            else:
                messages.add_message(request, messages.WARNING, 'Authorization FAILED.')
                return render(request, 'ninja/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'ninja/login.html', {'form': form})

def user_logout(request):
    logout(request)
    print("LOGOUT HAPPENED")
    return redirect('login')


def user_sign_up(request):
    # Reinventing the bicycle for educational purposes
    #   in production should use django way
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['password_repeat']:
                messages.add_message(request, messages.WARNING, 'Passwords do NOT match')
                return render(request, 'ninja/signup.html', {'form': form})

            messages.add_message(request, messages.SUCCESS, 'SignUp successful! Please login')
            return redirect('login')
            # TODO: logic for user object creation


        # if form is not valid, whatever that means
        else:
            messages.add_message(request, messages.WARNING, 'Form validation failed << DEBUG purposes')
            return render(request, 'ninja/signup.html', {'form': form})
    # if method == 'GET' just display the form
    else:
        form = SignUpForm()
        return render(request, 'ninja/signup.html', {'form': form})

def index(request):

    #     shows a  simple list of all courses
    #     in the database
    just_a_variable = Course.objects.all()
    context = {"just_a_variable" : just_a_variable}
    return render(request, "ninja/index.html", context)


def showSections(request):

    comp_courses = Course.objects.filter(course_subject='COMP')

    comp_sections = Section.objects.filter(course__course_subject='COMP')

    return render(request, "ninja/index.html", {"comp_sections" : comp_sections})