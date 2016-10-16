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

    subject = models.CharField(max_length=20)
    course_level = models.CharField(max_length=10)
    units = models.FloatField()


    class Meta:
        unique_together =('subject', 'course_level')


class Section(models.Model):

    course = models.ForeignKey(Course, related_name="section")
    section_number = models.CharField(max_length=10, primary_key=True)


class SectionSchedule(models.Model):

    section = models.ForeignKey(Section)
    days = models.CharField(max_length=10)

    section = models.ForeignKey(Section) # <Section object>
    days = models.CharField(max_length=10) # "MTWHFS"
    time_start = models.TimeField(blank=True)
    time_end = models.TimeField(blank=True)
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)


class Instructor(models.Model):
	# Instructor model is referenced by the Section Details model
	
    name = models.CharField(max_length=100)


class Prerequisites(models.Model):
    # Prerequisite model is connected to the courses table
    # consists of two fields for verifying if a specific course
    # meets all prerequisites required before taking the class

    main_course = models.ForeignKey(Course)
    prerequisite_course = models.ForeignKey(Course)
	

class Subject(models.Model):
	# Subject model holds the subject name and description
	# which is referenced in the courses model
	
    name = models.CharField(max_length=75)
    description = models.TextField()
