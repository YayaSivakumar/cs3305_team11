# script name: get_pdf_metadata.py

def get_metadata_pdf(file_path: str) -> object:
    pass


class PDF:

    def __init__(self, title, author, date):
        self._title = title
        self._author = author
        self._creation_date = date

    def __str__(self):
        return f'Subject: {self.subject}\nAuthor: {self.author}\nDate: {self.date}\n'

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def creation_date(self):
        return self._creation_date
