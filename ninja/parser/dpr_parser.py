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

        get_subjects(str)
        return str


    def get_subjects(dpr_text):
        pattern1 = re.compile(r'(GE.*:)')
        pattern2 = re.compile(r'\s')
        result = re.findall(pattern2, dpr_text)
        print (result)
        #return result


#==============================================================================#
    logging.debug('START File Parsing')

    DPR_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SampleDPR.pdf')

    # This is a path to the txt file containing all subject abbreviations
    #SUBJECTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_subjects.txt')

    # get a raw text from the pdf
    text_source = pdf_to_txt(DPR_FILE_NAME)

    output_text = open('dpr_output.txt', 'wb')
    output_text.write(text_source.encode('utf-8'))
    output_text.close()

if __name__ == '__main__':
    main()
