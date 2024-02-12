from python.model.FileSystemNodeModel import File


class Document(File):
    def __init__(self, path, cache):
        super().__init__(path, cache)
        self._filetype = self.path.split('.')[-1]
        self._title = None
        self._authors = None
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

    def _populate_document_metadata(self):
        """Populate the document with its metadata."""
        if self._filetype == 'pdf':
            self._populate_pdf_metadata()
        elif self._filetype == 'docx':
            self._populate_docx_metadata()

    def _populate_pdf_metadata(self):
        """Populate the document with its metadata."""
        pass

    def _populate_docx_metadata(self):
        """Populate the document with its metadata."""
        pass

