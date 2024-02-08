from python.model.FileSystemNodeModel import File

class Music(File):
    def __init__(self, path, cache):
        super().__init__(path, cache)
        self._filetype = 'music'
        self._artist = None
        self._album = None
        self._title = None
        self._track_number = None
        self._genre = None
        self._year = None

    @property
    def artist(self) -> str:
        """The artist of the music file."""
        return self._artist

    @artist.setter
    def artist(self, a: str) -> None:
        self._artist = a

    @property
    def album(self) -> str:
        """The album of the music file."""
        return self._album

    @album.setter
    def album(self, a: str) -> None:
        self._album = a

    @property
    def title(self) -> str:
        """The title of the music file."""
        return self._title

    @title.setter
    def title(self, t: str) -> None:
        self._title = t

    @property
    def track_number(self) -> str:
        """The track number of the music file."""
        return self._track_number

    @track_number.setter
    def track_number(self, tn: str) -> None:
        self._track_number = tn

    @property
    def genre(self) -> str:
        """The genre of the music file."""
        return self._genre

    @genre.setter
    def genre(self, g: str) -> None:
        self._genre = g

    @property
    def year(self) -> str:
        """The year of the music file."""
        return self._year

    @year.setter
    def year(self, y: str) -> None:
        self._year = y

music_file = Music('path', 'cache')
print(music_file.artist)
music_file.year = '2021'
