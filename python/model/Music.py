from python.model.FileSystemNodeModel import File   # Importing the File class from FileSystemNodeModel
import os       # Importing the os module for file operations
import shutil      # Importing the shutil module for file moving operations
from mutagen.easyid3 import EasyID3      # Importing EasyID3 from mutagen for reading ID3 tags


def get_all_file_paths(path: str) -> list[str]:
    """
    Function to get the paths of all audio files in a directory and its subdirectories.

    @params
    path: str: absolute path of directory to be traversed
    ret: list[str]: list of absolute paths of audio files
    """
    audio_extensions = ['.mp3', '.wav', '.aac', '.m4a']    # List of audio file extensions
    files_list = []      # List to store teh absolute paths of audio files
    
    # walk through all the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in audio_extensions:      # Check if the file has an audio extension
                files_list.append(os.path.join(root, file))     # Add teh absolute path to the files list
    return files_list


class Music(File):
    """
    Constructor for the Music class

    @params
    path: str: absolute path of the music file
    cache: object: cache object
    artist: str: artist name (default: None)
    track_name: str: track name (default: None)
    album: str: album name (default: None)
    year: str: year (default: None)
    """
    def __init__(self, path: str, cache, artist=None, track_name=None, album=None, year=None):
        super().__init__(path, cache)     # Call the constructor of the parent class
        self._artist = artist             # Initialize artist attribute
        self._track_name = track_name     # Initialize track name attribute
        self._album = album               # Initialize album attribute
        self._year = year                 # Initialize year attribute

    def __repr__(self):
        """Representation of a Music object"""
        return f"MusicFile(path={self.path}, artist={self.artist}, track_name={self.track_name}, album={self.album}, year={self.year})"

    # Property getters and setters for artist, track_name, album, and year attributes

    @property
    def artist(self) -> str:
        """The artist of the music file."""
        return self._artist

    @artist.setter
    def artist(self, a: str) -> None:
        self._artist = a

    @property
    def track_name(self) -> str:
        """The name of the track."""
        return self._track_name

    @track_name.setter
    def track_name(self, t: str) -> None:
        self._track_name = t

    @property
    def album(self) -> str:
        """The album of the music file."""
        return self._album

    @album.setter
    def album(self, al: str) -> None:
        self._album = al

    @property
    def year(self) -> int:
        """The year of the music file."""
        return self._year

    @year.setter
    def year(self, y: str) -> None:
        self._year = y
        
    def get_music_data(self):
        """
        Method to retrieve metadata from audio files.

        @return
        list[Music]: List of Music objects containing metadata
        """
        music_files = []     # List to store Music objects
        file_paths = get_all_file_paths(self.path)        # Get paths of all audio files
        for file in file_paths:
            extension = file.split('.')[-1]
            if extension in ['wav', 'mp3', 'aac']:
                try:
                    audio = EasyID3(file)       # Read ID3 tags from audio file
                    if audio:
                        # Extract metadata from ID3 tags
                        self._artist = audio['artist'][0] if 'artist' in audio else None
                        self._album = audio['album'][0] if 'album' in audio else None
                        self._track_name = audio['title'][0] if 'title' in audio else None
                        self._year = audio['year'][0] if 'year' in audio else None
                        # Create Music object with metadata and add to the list
                        music_files.append(Music(path=file, cache=self.cache, artist=self._artist, track_name=self._track_name, album=self._album, year=self._year))
                    else:
                        print(f"No metadata found in the file: {file}")
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
        return music_files

    def organize_music(self, organize_by: str):
        """
        Method to organize music files into directories based on metadata.

        @params
        organize_by: str: criteria for organizing (artist, album, year)
        """
        
        if not os.path.exists(self.path):
            print(f"Directory '{self.path}' does not exist.")
            return

        music_files = self.get_music_data()   # Retrieve music metadata
        for audio_file in music_files:
            try:
                if organize_by == 'artist':
                    target_directory = os.path.join(self.path, audio_file.artist)    # Target directory based on artist
                elif organize_by == 'album':
                    target_directory = os.path.join(self.path, audio_file.album)     # Target directory based on album
                elif organize_by == 'year' and self.year is not None:
                    target_directory = os.path.join(self.path, str(audio_file.year))   # Target directory based on year
                else:
                    print(f"Invalid organize_by value: {organize_by}")
                    return

                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)     # Create target directory if it doesn't exist

                # Move the audio file to the target directory
                shutil.move(audio_file.path, os.path.join(target_directory, os.path.basename(audio_file.path)))
                print(f"Moved {audio_file.path} to {target_directory}")

            except Exception as e:
                print(f"Error organizing file {audio_file.path}: {e}")


if __name__ == '__main__':
    music_dir = "/home/evelynchelsea/test music"     # Directory containing music files
    music_collection = Music(music_dir, 'cache')   # Create Music collection object
    music_collection.organize_music('album')             # Organize music files by album
