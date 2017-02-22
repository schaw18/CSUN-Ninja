from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os, re, logging
from ..models import Course

def main():

    def pdf_to_txt(filename):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        
        fp = open(filename, 'rb')
        if fp:
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
                interpreter.process_page(page)

            str = retstr.getvalue()

            fp.close()
            device.close()
            retstr.close()
            return str
        else:
            logging.ERROR('ERROR: couldn\'t open PDF source file')
            return None

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
            subject = subject.replace('  ', '')
            text_source = text_source.replace("  " + subject, '\n' + subject)
            #print(subject)
        return text_source

    def clean_dpr(dpr_text):
        page_pattern = re.compile(r'\nPage\s\d{1,}\sof\s\d{1,}\n+\x0c')

        # remove page numbers
        for page_line in re.findall(page_pattern, dpr_text):
            dpr_text = dpr_text.replace(page_line, '')

        # clean up formatting
        dpr_text = dpr_text.replace('  ,', ',')
        dpr_text = dpr_text.replace(' ,', ',')
        dpr_text = dpr_text.replace(',\n', '\n')
        dpr_text = dpr_text.replace(' \n', '\n')
        dpr_text = dpr_text.replace("\n\n", '\n')

        return dpr_text

    def udge_pattern_search(dpr_text):
        ge_block_pattern = re.compile(r'GE.*:\s(?:\w+\s?\w+\s+(?:\d{1,3}[A-Z]*?(?:,|\s))+)+')
        subject_pattern = re.compile(r'(\w+\s?\w+)\s+')
        ge_course_pattern = re.compile(r'(?P<course_subject>\w+\s?\w+)\s+'
        			       r'(?P<course_level>\d{1,3}[A-Z]*?)')
        ge_set = set()
        
        ge_blocks = re.findall(ge_block_pattern, dpr_text)

        for ge_block in ge_blocks:
            ge_block = re.split('\n', ge_block)

            # 1st element in list is the GE type
            ge_type = ge_block[0]

            for course_list in ge_block[1:len(ge_block)]:
                subject = re.findall(subject_pattern, course_list)
                if subject:
                    course_list = course_list.replace(',', '\n' + subject[0] + ' ')
                    course_list = course_list.replace('  ', ' ')
                    course_list = re.split('\n', course_list)
                    for course in course_list:
                        ge_set.add(course)

        for course in ge_set:
            mo = ge_course_pattern.search(course)
            if mo:
                model_population(mo)
            else:
                logging.debug('FAILED to find PATTERN in the course: \"%s\"\n' % course)

                
    def courses_taken_search(dpr_text):
        courses_taken_pattern = re.compile(r'^\s*(?P<year_taken>\d{2})'
                                           r'(?P<semester_taken>[A-Z]{2})\s+'
                                           r'(?P<course_subject>\w+\s?\w+)\s+'
                                           r'(?P<course_level>\d{1,3}[A-Z]*?)$', re.MULTILINE)
        courses_taken = re.finditer(courses_taken_pattern, dpr_text)
        
        #for mo in courses_taken:
            #taken_model_population(mo)

    def model_population(mo):
        try:
            course_subject = mo.group('course_subject')
            course_level = mo.group('course_level')
        except AttributeError:
            logging.warning('FAILED to split re.object to groups')

#==============================================================================#

    # This is a path to the source PDF file
    DPR_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SampleDPR.pdf')
    # This is a path to the txt file containing all subject abbreviations
    SUBJECTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_subjects.txt')

    logging.debug('START File Parsing')

    # get a set of all course abbreviations(from a file)
    set_of_course_subjects = load_subjects(SUBJECTS_FILE)
    # get a raw text from the pdf
    text_source = pdf_to_txt(DPR_FILE_NAME)

    # split to lines at every occurrence of the subject abbreviation
    text_source = cut_by_subject(text_source, set_of_course_subjects)

    # clean up and filter dpr text
    text_source = clean_dpr(text_source)

    # check for classes taken
    courses_taken_search(text_source)
    
    # check that the UDGE requirement is met
    udge_pattern_search(text_source)

    # output to file (for debugging purposes)
    output_text = open('dpr_output.txt', 'w')
    output_text.write(text_source)
    output_text.close()

    logging.debug('FINISH File Parsing')

if __name__ == '__main__':
    print(sys.path)
    #main()
