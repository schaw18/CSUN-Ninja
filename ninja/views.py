from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, SignUpForm, FilterForm
from .models import *

# local exports
from .helpers import login_logout


def user_login(request):
    # if successful redirects to index
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
                    return redirect('index')

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
    return redirect('login')


def user_sign_up(request):
    # Reinventing the bicycle for educational purposes
    #   in production should use django validation.
    #   Creates the most basic user, without any confirmations
    #   and with very limited validation
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if login_logout.user_exists(cd['username']):
                messages.add_message(request, messages.WARNING, 'User exists. Please chose different username')
                return render(request, 'ninja/signup.html', {'form': form})

            if cd['password'] != cd['password_repeat']:
                messages.add_message(request, messages.WARNING, 'Passwords do NOT match')
                return render(request, 'ninja/signup.html', {'form': form})

            u = User(username=cd['username'], email=cd['password'])
            u.set_password(cd['password'])
            u.save()

            messages.add_message(request, messages.SUCCESS, 'SignUp successful! Please login')
            return redirect('login')


        # if form is not valid, whatever that means
        else:
            messages.add_message(request, messages.WARNING, 'Form validation failed << DEBUG purposes')
            return render(request, 'ninja/signup.html', {'form': form})
    # if method == 'GET' just display the form
    else:
        form = SignUpForm()
        return render(request, 'ninja/signup.html', {'form': form})

def flush_db(request):
    from .helpers import db_erase
    db_erase.erase()
    messages.add_message(request, messages.INFO, 'Database erased')

    return redirect('index')

def update_classes(request):
    from .parser import pdf_parser
    pdf_parser.main()
    messages.add_message(request, messages.INFO, 'Classed updated')

    return redirect('index')

def index(request):

    #     shows a  simple list of all courses
    #     in the database
    all_courses = Course.objects.all()
    context ={}
    if request.user.is_authenticated:
        print(request.user)
        filter, created =  UserFilters.objects.get_or_create(user=request.user)
        days_list = filter.days_list()

        context = {"all_courses" : all_courses,
               "days_list": days_list}
    return render(request, "ninja/index.html", context)



@login_required
def filters(request):

    user = request.user
    filter, created = UserFilters.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = FilterForm(request.POST, instance=filter)
        if form.is_valid():
            form.save()


            messages.add_message(request, messages.INFO, 'Filter saved!')
            return render(request, 'ninja/filters.html', {'form': form})
        else:
            messages.add_message(request, messages.WARNING, 'Form validation failed << DEBUG purposes')
            return render(request, 'ninja/filters.html', {'form': form})

    else:
        form = FilterForm(instance=filter)
        return render(request, 'ninja/filters.html', {'form': form})


def showSections(request):

    comp_courses = Course.objects.filter(course_subject='COMP')

    comp_sections = Section.objects.filter(course__course_subject='COMP')

    return render(request, "ninja/index.html", {"comp_sections" : comp_sections})