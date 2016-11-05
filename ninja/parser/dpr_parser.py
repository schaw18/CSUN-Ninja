import PyPDF2
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

    def pattern_search(dpr_text):
        #course_pattern = re.compile(r'(?:\n| +)([A-Z]{2,4}|[A-Z]{1,2} [A-Z])(?: +)(\d{3}(?:[A-Z]| )?(?:,|\n|,\n))+')
        #course_pattern = re.compile(r'''
        #(?:\n| +)           # New line or spaces precede course name
        #([A-Z]{2,4}         # Course name can be 2-4 letters
        #|[A-Z]{1,2} [A-Z])  # or 1-2 letters followed by 1 letter
        #(?: +)              # Course name followed by at least 1 space
        #\d{3}              # Course number must be 3 digits
        #?:[A-Z]| )?        # Followed by an optional letter or space
        #?:,|\n|,\n)        # but must end with , or new line or both
        #)+                  # and can repeat more than once
        #''', re.VERBOSE)

        ge_pattern = re.compile(r'(?:GE(?:[A-Z]| | &)*:)(?:.|\n)*(?:GE(?:[A-Z]| | &)*:)')

        results = re.findall(ge_pattern, dpr_text)

        for result in results:
            print(result)

        #print(re.findall(ge_pattern, dpr_text))

#==============================================================================#
    logging.debug('START File Parsing')

    # This is a path to the source PDF file
    DPR_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SampleDPR.pdf')

    # get a raw text from the pdf
    text_source = pdf_to_txt(DPR_FILE_NAME)

    # begin pattern matching
    pattern_search(text_source)

    # output to file (for debugging purposes)
    #output_text = open('dpr_output.txt', 'w')
    #output_text.write(text_source)
    #output_text.close()


if __name__ == '__main__':
    main()
