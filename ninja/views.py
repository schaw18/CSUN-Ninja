from django.shortcuts import render
from .models import *

def ShowAll(request):

    just_a_variable = Course.objects.all()

    context = {"just_a_variable" : just_a_variable}

    return render(request, "ninja/index.html", context)