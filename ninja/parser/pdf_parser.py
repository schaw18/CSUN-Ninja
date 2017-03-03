import PyPDF2
import re, os, logging
import boto3
import time
import datetime
import urllib.request

from ..models import Course, Section, SectionSchedule
from django.db.utils import IntegrityError

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    )
def main():

    def print_a_list(source_list):
        # for debugging activities only
        for element in source_list:
            print(element)

    def clean_service_lines(text_source):
        """ need to identify and ignore metadata which appears on every page
            such as page number, date, notes and etc.
            :argument a raw text as
            :return list of "cleaned" lines """


        # one of these wors may appear in the service lines
        bad_words_pattern = re.compile(r'.*Classes|Northridge|NRPA\d{0,10}|'
                                       r'UndergraduateNote|Classes Open|Version: |'
                                       r'UndergraduateNote|CLASSES|Printed:.*')

        # These are not words, but dates, page numbers and etc
        # we don't want them neither

        bits_and_pieces_pattern = re.compile(r'Page|\sof\s|\d{1,10}\.\d{1,3}|'
                                             r'\d\d/\d\d/\d\d\d\d\s\d\d:\d\d:\d\d|'
                                             r'^\d{1,3}')

        text_source = text_source.replace('Program ID:', '\n')  # newline for the service string at the end of the page
        text_source = text_source.replace('Date:', ' Date:')  # add an extra space before the Date

        # creates a list out of a text file
        # every lines becomes an element of the list
        list_of_source_lines = text_source.split('\n')
        new_list_of_source_lines = []

        for line in list_of_source_lines:
            # check if this line contains any of the "bad" words
            # if it does - the line is a "service line" and needs to be ignored
            # and if it does not - append the line to the list of "good" lines for
            # further processing
            if not bad_words_pattern.search(line) and \
                    not bits_and_pieces_pattern.search(line):
                new_list_of_source_lines.append(line)

        if new_list_of_source_lines[0] == '':
            new_list_of_source_lines.pop(0)  # HACK, the 0 element somehow was a ''
        return new_list_of_source_lines

    def cut_by_subject(text_source, set_of_subjects):
        """there is a predefined list of course subjects
            and we assume that every time one of these subject appears in
            the text we need to parse - this is actually a new course.
            We add a newline before such "course subject", so it becomes actually a line.
            for example:
                COMP 456 blah-blah COMP 478 yada blach ART 123 blah... ->
                COMP 456 blah-blah
                COMP 478 yada... and so on
            this is not strictly necessary, but helps a lot to make the whole
            process easier to understand and work with.
            IMPORTANT: this assumption is actually incorrect, so we need a helper function
            to glue some (mistakenly cut) lines back
            """

        for subject in set_of_subjects:
            text_source = text_source.replace(subject, '\n' + subject)
            # print(subject)
        return text_source

    def glue_short_string_back(list_of_lines):
        # print_a_list(list_of_lines)
        '''some strings were cut my mistake, so we check their length, and if its suspiciously short
            we glue it to the next string
            example ASS 110 Description <will be cut by mistake here> ASS Room: Date'''
        new_list_of_courses = []
        temp = ''

        for course_line in list_of_lines:

            course_line.strip('')
            course_line = temp + course_line
            if len(course_line) < 50:
                temp = course_line

            else:
                new_list_of_courses.append(course_line)
                temp = ''
        return new_list_of_courses

    def load_subjects(filename):
        """takes a txt file of course subjects, cleans a bit
        and return a set of course subjects"""
        set_of_subjects = []
        with open(filename, 'r') as f:
            if f:
                for line in f:
                    if not line.startswith('#'):
                        set_of_subjects.append(line.strip('\"\',\n ') + '  ')
            else:
                logging.ERROR('ERROR: couldn\'t open Subject txt File')
        return set_of_subjects

    def pdf_to_txt(filename, FIRST_PAGE, LAST_PAGE):
        """
        :param filename:
        :param FIRST_PAGE:
        :param LAST_PAGE:
        :return: a dump of PDF as a string
        """
        src = ''
        pdf_file_object = open(filename, 'rb')
        if pdf_file_object:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)

            if FIRST_PAGE == LAST_PAGE == None:
                FIRST_PAGE = 0
                LAST_PAGE = pdf_reader.numPages

            for pageNum in range(FIRST_PAGE, LAST_PAGE):
                page_object = pdf_reader.getPage(pageNum)
                src += page_object.extractText()
            pdf_file_object.close()
            return src.lstrip()
        else:
            logging.ERROR('ERROR: couldn\'t open PDF source file')
            return None



    def multi_section_parse(list_of_lines):
        # print_a_list(list_of_lines)

        '''If a line has only one COURSE ABBREVIATION
            but multiple 'Date:' entries - that means this course has multiple sections
            so we expand this sections like they are courses on their own
            returns a LIST of strings'''

        list_of_classes = []
        for src in list_of_lines:
            left_bound = src.find('Date')
            # print("LEFT BOUND:",left_bound)
            for i in range(src.count('Date') + 1):
                if i > 1:
                    right_bound = src.rfind('Date')
                    # print("RIGHT BOUND:", right_bound)
                    a = src[:left_bound] + src[right_bound:]
                    # print("Slice:", a)
                    src = src[:right_bound]
                    list_of_classes.append(a)
            list_of_classes.append(src)

        return list_of_classes

    def pattern_search(list_of_lines):
        """ goes througth all lines one by one and tries to match
         predefined a pattern. If there is a match - > send this line
         (in form of re object) to the function that will record it in the
          database.
          If there is no match - complain about it, since the assumtion is:
          at this point all lines we are working with contain info about courses

        """
        pattern = re.compile(r'^\s*(?P<course_subject>\w+\s?\w+)\s+'
                             r'(?P<course_level>\d{1,3}[A-Z]*?)\s+'
                             r'(?P<course_title>[0-9A-Z\s!@#$^&*,.()/&-+:+~`\-?\'\"]+)\s*'
                             r'(?P<session>Regular)\s+'
                             r'(?P<section_number>\d\d\w?\d?)\s+'
                             r'(?P<course_type>\w{3,10})\s+'
                             r'(?P<class_number>\d{3,6})\s+'
                             r'(?P<enrollment_available>\d{0,4})\s+'
                             r'(?P<enrollment_max>\d{0,4})'
                             r'\s+(?P<units>\d\.?\d?\d?)\s+'
                             r'Date:\s+(?P<date_start>[0-9/]+)\s+-\s+'
                             r'(?P<date_end>[0-9/]+)\s+'
                             r'Time:\s+(?P<time>[0-9AMP :-]+)\s'
                             r'Days:\s+(?P<days>[A-Za-z]+)\s+'
                             r'Room:\s+(?P<room>[A-Za-z0-9@\- ]+)\s+'
                             r'Instructor:\s+(?P<instructor>[A-Za-z, ]+)')

        for line in list_of_lines:
            mo = pattern.search(line)
            if mo:
                print(mo.group(0))
                model_population(mo)
            else:
                logging.debug('FAILED to find PATTERN in the\n%s' % line)

        return

    def model_population(mo):
        # logging.debug('ENTER: model population()')

        try:

            course_subject = mo.group('course_subject')
            # underscore spaces in abbreviations, because they will
            # be directly used as an URLs.
            # TODO: actually there is no need for _, I can just include space into url regex

            course_level = mo.group('course_level')
            course_title = mo.group('course_title').strip()
            course_type = mo.group('course_type')
            session = mo.group('session')
            class_number = mo.group('class_number')
            section_number = mo.group('section_number')[:2]
            current_enrolment = mo.group('enrollment_available')
            max_enrollment = mo.group('enrollment_max')
            units = mo.group('units')
            date_start = mo.group('date_start')
            date_end = mo.group('date_end')
            time = mo.group('time')
            days = mo.group('days')
            room = mo.group('room').strip()
            instructor = mo.group('instructor')
            days = days.replace('Th', 'H').replace('Tu', 'T').replace('Sa', 'S')

        except AttributeError:
            logging.warning('FAILED to split re.object to groups')


        # changes the format of the times and dates representation
        try:
            date_end = datetime.datetime.strptime(date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
            date_start = datetime.datetime.strptime(date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
            time_start, time_end = time_parsing(time)

        except:
            logging.warning('FAILED to TIME/DATE format change')

        # if a such a course exist - update its fields
        # otherwise - create a new one
        try:

            course, created = Course.objects.update_or_create(
                course_subject=course_subject,
                course_level=course_level,
                course_title=course_title,
                course_type=course_type,
                course_units=units,
            )
            course.save()

        except IntegrityError:
            logging.warning('FAILED to CREATE/UPDATE Course %s %s %s %s %s' %(course_subject,
                                                                     course_level,
                                                                     course_title,
                                                                     course_type,
                                                                     units))


        # creates a section for a given course
        try:
            course = Course.objects.get(course_subject=course_subject, course_level=course_level)

            section, created = Section.objects.update_or_create(
                course=course,
                class_number=class_number,
                section_number=section_number,
                # for the future
                # section_max_enrollment=max_enrollment,
                # section_current_enrollment=current_enrolment,
            )
            section.save()

        except IntegrityError:
            logging.warning('FAILED to CREATE/UPDATE Section %s' %(class_number))

        # add a Schedule to a given section
        # TODO: has a bug! if schedule changes -> adds a new schedule but doesnt delete old one
        try:
            # print("Trying to add Section Schedule")

            section = Section.objects.get(class_number=class_number)
            section_schedule, created = \
                SectionSchedule.objects.update_or_create(
                    section=section,
                    date_start=date_start,
                    date_end=date_end,
                    time_start=time_start,
                    time_end=time_end,
                    days=days,
                    room=room,
                    instructor=instructor,
                )
            section_schedule.save()


        except IntegrityError:
            logging.warning("FAILED to CREATE/UPDATE Section Schedule%s-%s-%s"(class_number, section_number, days))
            # logging.debug("time %s-%s date %s %s" %(time_start, time_end, date_start, date_end))

    def time_parsing(time_string):

        '''Gets string like 01:30AM - 2:15PM
        and yields 01:30 and 14:15'''

        pattern = re.compile(r'([0-9 :AMP]+)\s-\s([0-9 :AMP]+)')

        times = pattern.search(time_string)
        if times:
            time_start = times.group(1)
            time_end = times.group(2)
        else:
            time_start = time_end = None

        try:
            if time_start:
                time_start = time_start.strip()
                time_in = datetime.datetime.strptime(time_start, '%I:%M%p')
                time_start = str(time_in.hour) + ":" + str(time_in.minute)
            if time_end:
                time_end = time_end.strip()
                time_in = datetime.datetime.strptime(time_end, '%I:%M%p')
                time_end = str(time_in.hour) + ":" + str(time_in.minute)
        except ValueError:
            logging.debug('Something wrong with TIME parsing')
        return time_start, time_end

    def schedule_download_and_archive(FILE_SAVE_PATH):
        """downloads a pdf of schedule and saves it locally,
        if a local file already exists - deletes it,
        then timesmaps it with UNIX time and
        stores in in S3"""


        URL_OF_SCHEDULE_PDF = 'http://www.csun.edu/OpenClasses'

        # if a local copy exists - delete it
        if os.path.isfile(FILE_SAVE_PATH):
            os.unlink(FILE_SAVE_PATH)

        logging.debug('START File DOWNLOAD')
        urllib.request.urlretrieve(URL_OF_SCHEDULE_PDF, FILE_SAVE_PATH)
        timestamp = int(time.time())

        # waits until the file appears
        # for debug puproses only, probably wont be needed
        if not os.path.isfile(FILE_SAVE_PATH):
            print('WAITING FOR THE FILE TO DOWNLOAD')
            time.sleep(1)

        logging.debug('UPLOADING to S3')
        timestamped_filename = "{}_openclasses.pdf".format(str(timestamp))
        # s3 = boto3.resource('s3')
        # s3.Object('csunninja', timestamped_filename).put(Body=open(FILE_SAVE_PATH, 'rb'))
        return



    def launch():


        # Download the file from `URL_OF_SCHEDULE_PDF` and save it locally under `FILE_SAVE_PATH`:
        FILE_SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OpenClasses.pdf')

        # This is a path to the source PDF file
        PDF_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OpenClasses.pdf')

        # This is a path to the txt file containing all subject abbreviations
        SUBJECTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_subjects.txt')

        # download a fresh version of a schedule, save it locally
        # then timestamp it and send to S3 bucket
        schedule_download_and_archive(FILE_SAVE_PATH)

        logging.debug('START File Parsing')
        # What pages of the source PDF file to pass
        FIRST_PAGE = None
        LAST_PAGE = None # if both are None - then the whole document will be parsed

        # get a set of all course abbreviations(from a file)
        set_of_course_subjects = load_subjects(SUBJECTS_FILE)
        # get a raw text from the pdf
        text_source = pdf_to_txt(PDF_FILE_NAME, FIRST_PAGE, LAST_PAGE)

        # split to lines at every occurrence of the subject abbreviation
        text_source = cut_by_subject(text_source, set_of_course_subjects)

        # clean service lines and get a LIST of clean lines
        list_of_lines = clean_service_lines(text_source)

        # sometimes splitting makes an error (if abbreviation appears in the title
        # of the course) so we just glue an  extra  line back
        list_of_lines = glue_short_string_back(list_of_lines)

        # attach course information to each section
        # AAA 100 Date:11/11/11 Date:22/22/22 --->
        # AAA 100 Date:11/11/11
        # AAA 100 Date:22/22/22
        list_of_lines = multi_section_parse(list_of_lines)

        pattern_search(list_of_lines)

        # print_a_list(list_of_lines)
        logging.debug("FINISHED: Files parsing and database population")

    launch()


if __name__ == '__main__':
    main()
