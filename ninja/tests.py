from django.test import TestCase, RequestFactory
from .views import *
from .models import *


class ListOfCourses(TestCase):
    """creates 6 (SIX) employees
        then counts waht beeing passed from the template"""

    def setUp(self):
        # creating courses
        Course.objects.create(subject = "COMP", course_level = "100")
        Course.objects.create(subject = "COMP", course_level = "200")
        Course.objects.create(subject = "COMP", course_level = "300")
        Course.objects.create(subject = "COMP", course_level = "400")
        Course.objects.create(subject = "ART", course_level = "400")
        Course.objects.create(subject = "ART", course_level = "500")

        self.factory = RequestFactory()



    def test_count_couses(self):

        request = self.factory.get('/', {})
        print(ShowAll(request))