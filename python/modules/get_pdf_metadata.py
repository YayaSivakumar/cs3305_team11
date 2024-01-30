# script name: get_pdf_metadata.py
import pdfreader
from helper_funcs import PDF


def get_metadata_pdf(file_path: str, citing_style) -> object:
    # open file
    file = open(file_path, 'rb')

    # get all metadata from file into dict
    md_dict = pdfreader.PDFDocument(file).metadata

    '''
    code to enter in missing metadata from APIs
    (Author, Title, CreationDate)
    '''

    # create PDF object from metadata
    pdf_obj = PDF(md_dict['Title'], md_dict['Author'], md_dict['CreationDate'])
    print(pdf_obj)

def create_harvard_citing(pdf_obj: PDF) -> str:
    pass

def create_apa_citing(pdf_obj: PDF) -> str:
    pass

def create_mla_citing(pdf_obj: PDF) -> str:
    pass

def create_chicago_citing(pdf_obj: PDF) -> str:
    pass


if __name__ == '__main__':
    get_metadata_pdf('/Users/yachitrasivakumar/Documents/pdf_test.pdf', create_chicago_citing)