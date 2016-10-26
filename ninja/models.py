from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    # No private info should be stored.
    #   This model is exclusively a handle to helper methods.
    #   Probably there is a better way, but will do for now.
    user = models.OneToOneField(User)

    def courses_on_short_list(self):
        # returns a set of course objects from the short list
        pass

    def courses_staged_for_registry(self):
        # returns a set of course objects
        #   that are staged for registry by the student
        pass

    def sections_short_list(self):
        # returns a set of section objects from
        # short list
        pass

    def sections_staged_for_registry(self):
        # returns a set of section objects from
        # short list
        pass

    def sections_staged_for_registry_at_this_day(self, day):
        # returns section objects staged for registry
        # and scheduled for a given day
        pass

    def sections_on_short_list_at_this_day(self, day):
        # returns section objects from short list
        # and scheduled for a given day
        pass



class Course(models.Model):
    # id field will be created automatically, but it
    #   not really informative, so we will enforce uniqueness in two fields
    #   this is questionable approach however

    course_subject = models.CharField(max_length=20)  # COMP
    course_level = models.CharField(max_length=10)  # 101/L
    course_title = models.CharField(max_length=200)  # Computer literacy and such
    course_type = models.CharField(max_length=20)  # Lecture
    course_units = models.FloatField()

    class Meta:
        unique_together = ('course_subject', 'course_level')


class Section(models.Model):
    course = models.ForeignKey(Course, related_name="section")  # <Course object>
    class_number = models.CharField(max_length=10, primary_key=True)  # 543563
    section_number = models.CharField(max_length=10)  # 1 or 2 or 3

    def has_conflict(self, class_number):
        # accepts a class_number and decides if this class causes schedule conflict
        # return TRUE is it does
        pass

    def __str__(self):
        return self.class_number


class SectionSchedule(models.Model):
    # one section will have several schedules in sense of "sessions"
    #   for example if the section goes from 1200-1300 and then 1330-1430
    #   then two "schedules" are needed

    section = models.ForeignKey(Section, related_name="section_schedule")  # <Section object>
    room = models.CharField(max_length=20, blank=True)
    instructor = models.CharField(max_length=20)        # just a name as a string, no specifics
    days = models.CharField(max_length=10)              # "MTWHFS"
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)


class Instructor(models.Model):
    # currently deprecated
    # Instructor model is referenced by the Section Details model

    name = models.CharField(max_length=100)


class Prerequisites(models.Model):
    # is a tuple of Courses, as an one way relation
    # establishes if the first Course is a Prerequisite for the second one
    main_course = models.ForeignKey('Course')
    prerequisite_course = models.ForeignKey('Course', related_name='prereq')

    class Meta:
        unique_together = ('main_course', 'prerequisite_course')


class Subject(models.Model):
    # Subject model holds the subject name and description
    #   which is referenced in the courses model

    name = models.CharField(max_length=75)
    description = models.TextField()


class Corequisites(models.Model):
    # is a tuple of Courses, as an one way relation
    #   establishes if the first Course is a Prerequisite for the second one

    main_course = models.ForeignKey('Course')
    corequisite_course = models.ForeignKey('Course', related_name='coreq')


class CoursesTaken(models.Model):
    #  a relation, if exists  -> this user took the course
    user = models.ForeignKey(User)
    course_taken = models.ForeignKey(Course)


class SectionShortList(models.Model):
    # a relation, if exists  -> this user
    #   have chosen the section for further consideration
    #   Should reflect current availability of the section
    user = models.ForeignKey(User)
    section =  models.ForeignKey(Section)


class SectionStagedForRegistry(models.Model):
    # a relation, if exists  -> this user
    #   have chosen the section for registration
    #   Should reflect current availability of the section
    user = models.ForeignKey(User)
    section =  models.ForeignKey(Section)


class FAQ(models.Model):
    # don't really belong to this app, but will keep it here
    # for simplicity
    # eventually needs to be refactored
    question = models.CharField(max_length=200, primary_key=True)
    answer = models.CharField(max_length=500)

    def __init__(self):
        return self.question


# class UserFilters(models.Model):
#     user = models.OneToOneField(User)
#