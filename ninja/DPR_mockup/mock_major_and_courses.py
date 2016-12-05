# will create a Major with a description
# and associate courses from the Major Diagram to this course
# I need it for testing  purposes until actual DPR parser will be ready
import logging
import os

from ..models import Major, MajorCourse, Course

MAJORS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'majors.txt')
MAJOR_COURSES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'major_courses.txt')


def create_majors():
    # gets majors and their description from the text file (mock)
    # and loads into the database

    map_of_majors = dict()
    with open(MAJORS_FILE, 'r') as f:
        if f:
            for line in f:
                if line == "":
                    continue
                if not line.startswith('#'):
                    major = line.split(":")
                    map_of_majors[major[0].strip()] = major[1].strip()
        else:
            logging.ERROR('ERROR: couldn\'t open {}'.format(MAJORS_FILE))
    for k, v in map_of_majors.items():
        Major.objects.update_or_create(abbreviation=k,
                                       description=v)
    return


def load_major_courses():
    # loads mock info form the txt file
    # into the database
    # (actually the info is correct)
    # assumes that Majors are already created

    with open(MAJOR_COURSES_FILE, 'r') as f:
        if f:
            for line in f:
                if line == "":
                    continue
                if not line.startswith('#'):
                    major = line.split(",")
                    course_subject=major[0].strip()
                    course_level=major[1].strip()
                    major_abbreviation=major[2].strip()
                    # if such Major doesnt exist then it's
                    # probably a typo
                    # try:
                    major = Major.objects.get(abbreviation=major_abbreviation)
                    course = Course.objects.get(course_subject=course_subject,
                                                course_level=course_level)
                    MajorCourse.objects.update_or_create(course=course,
                                                             major=major)

                    #not critical, for info purposes only, so broad except
                    # except:
                    #     logging.ERROR('ERROR: there is no {} major'.format(major_abbreviation))

        else:
            logging.ERROR('ERROR: couldn\'t open {}'.format(MAJOR_COURSES_FILE))
    return
