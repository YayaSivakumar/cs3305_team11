from python.model.FileSystemNodeModel import File
from PyPDF2 import PdfReader
from docx import Document as Doc


class Document(File):
    def __init__(self, path, cache):
        super().__init__(path, cache)
        self._title = None
        self._authors = None
        self._keywords = None
        self._populate_document_metadata()

    @property
    def title(self):
        """Return the title of the document."""
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    def authors(self):
        """Return the authors of the document."""
        return self._authors

    @authors.setter
    def authors(self, value: list):
        self._authors = value

    @property
    def keywords(self):
        """Return the keywords of the document."""
        return self._keywords

    @keywords.setter
    def keywords(self, value: list):
        self._keywords = value

    def _populate_document_metadata(self):
        """Populate the document with its metadata."""
        if self.extension() == '.pdf':
            self._populate_pdf_metadata()
        elif self.extension() == '.docx':
            self._populate_docx_metadata()

    def _populate_pdf_metadata(self):
        """Populate the document with its metadata."""
        try:
            reader = PdfReader(self.path)
            info = reader.metadata
            self.authors = info['/Author'] if '/Author' in info else None
            self.title = info['/Title'] if '/Title' in info else None
        except Exception as e:
            print(e)

    def _populate_docx_metadata(self):
        """Populate the document with its metadata."""
        try:
            doc = Doc(self.path)
            core_properties = doc.core_properties
            self.authors = core_properties.author if core_properties.author else None
            self.title = core_properties.title if core_properties.title else None
            self.keywords = core_properties.keywords if core_properties.keywords else None
        except Exception as e:
            print(e)


if __name__ == "__main__":
    pass