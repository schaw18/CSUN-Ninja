from django.shortcuts import render
from .models import *


def ShowAll(request):

    #     shows a  simple list of all courses
    #     in the database
    just_a_variable = Course.objects.all()

    context = {"just_a_variable" : just_a_variable}
    print (render(request, "ninja/course_list.html", context).content)
    return render(request, "ninja/course_list.html", context)