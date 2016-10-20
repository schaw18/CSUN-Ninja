from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    # Student model holds all personal information
    # and User model will handle authentication/login only
    # but
    # relate all other models to User, not the Student

    user = models.OneToOneField(User)
    name =  models.CharField(max_length=100)
    csun_id_number = models.CharField(max_length=12, blank=True)



class Course(models.Model):

    # id field will be created automatically, but it
    # not really informative, so we will enforce uniqueness in two fields
    # this is questionable approach however

    course_subject = models.CharField(max_length=20)  # COMP
    course_level = models.CharField(max_length=10)  # 101/L
    course_title = models.CharField(max_length=200)  # Computer literacy and such
    course_type = models.CharField(max_length=20)  # Lecture
    course_units = models.FloatField()


    class Meta:
        unique_together =('course_subject', 'course_level')


class Section(models.Model):

    course = models.ForeignKey(Course, related_name="section") # <Course object>
    class_number = models.CharField(max_length=10, primary_key=True) # 543563
    section_number = models.CharField(max_length=10) # 1 or 2 or 3


class SectionSchedule(models.Model):

    days = models.CharField(max_length=10)
    section = models.ForeignKey(Section) # <Section object>
    room = models.CharField(max_length=20, blank=True)
    instructor = models.CharField(max_length=20)
    days = models.CharField(max_length=10) # "MTWHFS"
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)


class Instructor(models.Model):
	# Instructor model is referenced by the Section Details model
	
    name = models.CharField(max_length=100)


class Prerequisites(models.Model):
    # Prerequisite model is connected to the courses table
    # consists of two fields for verifying if a specific course
    # meets all prerequisites required before taking the class

    main_course = models.ForeignKey('Course')
    prerequisite_course = models.ForeignKey('Course', related_name='prereq')

	
    class Meta:
	    unique_together = ('main_course', 'prerequisite_course')
	

class Subject(models.Model):
	# Subject model holds the subject name and description
	# which is referenced in the courses model
	
    name = models.CharField(max_length=75)
    description = models.TextField()

    
class Corequisites(models.Model):
    # Corequisites model is connected to the courses table
    # consists of two fields for verifying if a specific course
    # meets all corequisites required before taking the class

    main_course = models.ForeignKey('Course')
    corequisite_course = models.ForeignKey('Course', related_name='coreq')