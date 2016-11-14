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
        ge_pattern = re.compile(r'GE.*:(?:\s+(?:[A-Z]{2,4}|[A-Z]{1,2} [A-Z]) +(?:\d{3}(?:[A-Z]{1,2})?(?:,|\n)?)+)+')

        results = re.findall(ge_pattern, dpr_text)
        for result in results:
            print(result)

    def clean_dpr(dpr_text):
        page_pattern = re.compile(r'\nPage\s\d{1,}\sof\s\d{1,}\n+\x0c')
        for page_line in re.findall(page_pattern, dpr_text):
            dpr_text = dpr_text.replace(page_line, '')

        dpr_text = dpr_text.replace('  ,', ',')
        dpr_text = dpr_text.replace(' ,', ',')
        dpr_text = dpr_text.replace(',\n', '\n')

        return dpr_text

#==============================================================================#
    logging.debug('START File Parsing')

    # This is a path to the source PDF file
    DPR_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SampleDPR.pdf')

    # get a raw text from the pdf
    text_source = pdf_to_txt(DPR_FILE_NAME)

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
