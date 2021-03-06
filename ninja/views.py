
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

# local exports
from django.views.decorators.csrf import csrf_exempt
import json

from .helpers import login_logout
from .forms import LoginForm, SignUpForm, FilterForm, DPRUploadForm
from .models import *

@login_required()
def return_all_required_sections(request, major='COMP'):
    courses_toward_major =  Course.objects.filter(majorcourse__major__abbreviation=major).exclude(coursestaken__user=request.user)
    return HttpResponse(courses_toward_major)

@login_required
def return_all_courses_taken_by_student(request):
    user  = User.objects.get(username=request.user)
    courses_taken = CoursesTaken.objects.filter(user=user).values_list('course_taken_id', flat=True)
    list_of_courses_taken =[]
    for course_taken in courses_taken:
        list_of_courses_taken.append(Course.objects.get(id=course_taken))

    return list_of_courses_taken



def return_all_sections_toward_major(request, major="COMP"):

    # at this stage all info is mocked and
    # the only major in existence is COMP

    # selects all sections that have enrollment < maximum
    # with corresponding courses in the list of courses required
    # towards the given major
    # serialized by the helper function

    from .endpoint.serialize_by_sections import serialize_by_sections
    from django.db.models import F

    major_courses =  Course.objects.filter(majorcourse__major__abbreviation=major)
    sec = Section.objects.filter(course__in=major_courses, section_current_enrollment__lt=F('section_max_enrollment'))
    result = serialize_by_sections(sec)
    return HttpResponse(result)


def load_mock_major_data(request):
    from .DPR_mockup.mock_major_and_courses import create_majors, load_major_courses
    create_majors()
    load_major_courses()
    messages.add_message(request, messages.SUCCESS, 'Mock major info loaded')
    return redirect('index')


@csrf_exempt
def user_login(request):
    # if successful redirects to index
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('in is valid')
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])

            if user is not None:

                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Authorization successful.')
                    return HttpResponse('validated')
                    #return redirect('index')
                    #return HttpResponseRedirect('ninja/dashboard.html')
                    #return render(request, 'ninja/dashboard.html')

                else:
                    messages.add_message(request, messages.INFO, 'This user is suspended')
                    return render(request, 'ninja/login.html', {'form': form})
            else:
                messages.add_message(request, messages.WARNING, 'Authorization FAILED.')
                return HttpResponse('Invalid Password')
                #return render(request, 'ninja/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'ninja/dashboard.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def user_sign_up(request):
    # Reinventing the bicycle for educational purposes
    #   in production should use django validation.
    #   Creates the most basic user, without any confirmations
    #   and with very limited validation
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('in post')
        if request.is_ajax():
           print('is ajax')
        if form.is_valid():
            cd = form.cleaned_data
            print('in is valid')
            if login_logout.user_exists(cd['username']):
                #messages.add_message(request, messages.WARNING, 'User exists. Please chose different username')
                return HttpResponse('User already exists!')
                #return render(request, 'ninja/signup.html', {'form': form})

            if cd['password'] != cd['password_repeat']:
                messages.add_message(request, messages.WARNING, 'Passwords do NOT match')
                return render(request, 'ninja/signup.html', {'form': form})
            print(cd['username'])
            u = User(username=cd['username'], first_name=cd['first_name'], last_name=['last_name'], email=cd['email'])
            u.set_password(cd['password'])
            u.save()

            #messages.add_message(request, messages.SUCCESS, 'SignUp successful! Please login')
            #return redirect('login')
            #return redirect('http://localhost:8080/ninja_490/csunninja/index.html')
            return HttpResponse('Account created successfully. Please log in!')


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
        filter_obj, created =  UserFilters.objects.get_or_create(user=request.user)
        days_list = filter_obj.days_list()

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


@csrf_exempt
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        print(request.FILES, request.POST)

        form = DPRUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print('is valid!')
            user=request.user
            newdoc = DPRfile(user = user, docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('dashboard'))
            #return HttpResponse('Document uploaded successfully!')
    else:
        form = DPRUploadForm() # A empty, unbound form

    # Load documents for the list page
    documents = DPRfile.objects.filter(user=request.user)

    # Render list page with the documents and the form
    return render(request, "ninja/dashboard.html", {'documents': documents, 'form': form} )

def dpr_parser(request):
    from .parser import dpr_parser

    context = {}

    if request.user.is_authenticated:
        dpr_parser.main(request)
        messages.add_message(request, messages.INFO, 'DPR Parsed')
        recommended_courses = CoursesRecommended.objects.filter(user=request.user).values('course_recommended__course_subject',
                                                                                          'course_recommended__course_level',
                                                                                          'course_recommended__course_title',
                                                                                          'course_recommended__course_units')
        context = {"recommended_courses" : recommended_courses}

    return JsonResponse({'result' : list(recommended_courses)})

@csrf_exempt
def returnRecomended(request):

    all_courses = Course.objects.all().values('course_subject', 'course_level')
    all_sections =  Section.objects.all()
    all_schedules =  SectionSchedule.objects.all().values('section__course__course_subject',
                                                          'section__course__course_level',
                                                          'section__course__course_title',
                                                          'section__course__course_units',
                                                          'section__class_number',
                                                          'instructor',
                                                          'time_start',
                                                          'time_end',
                                                          'date_end',
                                                          'date_start',
                                                          'room')
    # all_recommended = CoursesRecommended.objects.all()
    # all_available_recommended =  Course.objects.all().exclude(all_recommended)

    print(Section.objects.count())
    #return JsonResponse({'results': list(all_schedules)})
    return JsonResponse({'classes': [{'course': 'COMP 333', 'days': 'M / W 12:00-1:15', 'units': '3'},
                                     {'course': 'COMP 496', 'days': 'T / R 1:00-2:15', 'units': '3'}]})

@csrf_exempt
def dashboard(request):

    return render(request, "ninja/dashboard.html")
