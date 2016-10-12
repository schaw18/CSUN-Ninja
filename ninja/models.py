from django.db import models


class Course(models.Model):

    subject = models.CharField(max_length=20)
    course_level = models.CharField(max_length=10)


class Section(models.Model):

    course = models.ForeignKey(Course, related_name="section")
    section_number = models.CharField(max_length=10, primary_key=True)


class SectionSchedule(models.Model):

    section = models.ForeignKey(Section)
    days = models.CharField(max_length=10)


class Instructor(models.Model):
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
