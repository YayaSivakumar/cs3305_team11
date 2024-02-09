from python.model.FileSystemNodeModel import File


class Document(File):
    def __init__(self, path, cache):
        super().__init__(path, cache)