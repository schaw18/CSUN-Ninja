from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os, re, logging

def main():

    def pdf_to_txt(filename):
        fp = open(filename, 'rb')
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        str = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()

        return str

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

    def pattern_search(dpr_text):
        ge_pattern = re.compile(r'GE.*:\n(?:(?:[A-Z]{2,4}|[A-Z]{1,2} [A-Z])\s+(?:\d{3}(?:[A-Z]{1,2})?(?:,|\n))+)+')

        ge_list = re.findall(ge_pattern, dpr_text)
        #iterator = re.finditer(ge_pattern, dpr_text)

        for result in ge_list:
            print(result)

    def clean_dpr(dpr_text):
        page_pattern = re.compile(r'\nPage\s\d{1,}\sof\s\d{1,}\n+\x0c')

        # remove page numbers
        for page_line in re.findall(page_pattern, dpr_text):
            dpr_text = dpr_text.replace(page_line, '')

        # clean up formatting
        dpr_text = dpr_text.replace('  ,', ',')
        dpr_text = dpr_text.replace(' ,', ',')
        dpr_text = dpr_text.replace(',\n', '\n')
        dpr_text = dpr_text.replace("\n\n", '\n')

        return dpr_text

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

    # begin pattern matching
    pattern_search(text_source)

    # output to file (for debugging purposes)
    output_text = open('dpr_output.txt', 'w')
    output_text.write(text_source)
    output_text.close()

if __name__ == '__main__':
    main()
