import PyPDF2
import os, logging

def main():

    # Valera's pdf_to_txt method
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

#==============================================================================#
    logging.debug('START File Parsing')

    # What pages of the source PDF file to pass
    # if both are None - then the whole document will be parsed
    FIRST_PAGE = None
    LAST_PAGE = None
    #change
    # TODO: User will submit the DPR file
    DPR_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SampleDPR.pdf')
    # This is a path to the txt file containing all subject abbreviations
    SUBJECTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_subjects.txt')

    # get a raw text from the pdf
    text_source = pdf_to_txt(DPR_FILE_NAME, FIRST_PAGE, LAST_PAGE)

    output_text = open('dpr_output.txt', 'wb')
    output_text.write(text_source.encode('utf-8'))
    output_text.close()

if __name__ == '__main__':
    main()
