# script name: create_pdf_citation.py
from pdf2doi import pdf2doi
from helper_funcs import PDF
import requests


def create_pdf_citation(file_path: str, citing_style) -> str:
    # create PDF object
    pdf_obj = get_pdf_metadata(file_path)

    # create citation
    citation = citing_style(pdf_obj)
    return citation

def get_pdf_metadata(file_path: str) -> object:
    """
    function to get metadata from pdf file

    @params
    file_path: str: absolute path to pdf file
    ret: dict: dictionary of metadata
    """
    # get DOI value from pdf file
    doi_items = pdf2doi(file_path)
    doi = doi_items['identifier']

    # obtain values needed using DOI
    title, author_list, date = get_values_using_doi(doi)

    # create PDF object
    pdf_obj = PDF(title, author_list, date)
    print(pdf_obj)
    return pdf_obj

def get_values_using_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    author_list = []
    if response.status_code == 200:
        data = response.json()
        title = data['message']['title'][0]
        date = data['message']['created']['date-parts'][0]
        authors = data['message']['author']
        for author in authors:
            author_list.append((author.get('given'), author.get('family')))
    return title, author_list, date

def create_harvard_citing(pdf_obj: PDF) -> str:
    pass

def create_apa_citing(pdf_obj: PDF) -> str:
    pass

def create_mla_citing(pdf_obj: PDF) -> str:
    pass

def create_chicago_citing(pdf_obj: PDF) -> str:
    pass

if __name__ == '__main__':
    # create_pdf_citation('/Users/yachitrasivakumar/Documents/pdf_test.pdf', create_harvard_citing)
    get_pdf_metadata('/Users/yachitrasivakumar/Documents/pdf_test.pdf')