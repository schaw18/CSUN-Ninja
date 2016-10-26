from django.shortcuts import render
from .models import *


def ShowAll(request):

    #     shows a  simple list of all courses
    #     in the database
    just_a_variable = Course.objects.all()

    context = {"just_a_variable" : just_a_variable}
    return render(request, "ninja/course_list.html", context)


def showSections(request):

    comp_courses = Course.objects.filter(course_subject='COMP')

    comp_sections = Section.objects.filter(course__course_subject='COMP')

    return render(request, "ninja/forms.html", {"comp_sections" : comp_sections})