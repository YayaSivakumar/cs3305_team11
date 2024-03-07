from __future__ import annotations
import os
from datetime import datetime
import shutil
import hashlib
import pyheif

from PyQt5.QtCore import QRunnable, QThreadPool

# music imports
from mutagen.easyid3 import EasyID3  # Importing EasyID3 from mutagen for reading ID3 tags

# image imports
import numpy as np
import pandas as pd
import subprocess
import PIL.Image
from PIL.ExifTags import TAGS


class FileSystemNode:
    """Represents a file or directory in the file system."""

    def __init__(self, path: str, cache: FileSystemCache, parent, size = None):
        self.path = path
        self.name = None
        self.revert_path = path
        self.cache_timestamp = None
        self.cache = cache
        self.parent = parent if parent else None
        self.children = []
        self.size = size

    def find_node(self, name: str):
        """Recursively find a node by name."""
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_node(name)
            if found:
                return found
        return None

    def find_node_from_cache(self, name: str) -> FileSystemNode:
        try:
            return self.cache[name]
        except KeyError:
            raise Exception(f"File {name} not found.")

    def print_tree(self, level=0):
        """Print the tree structure.
            Level is used for recursive call, param not to be used for testing per say
        """
        print('  ' * level + self.name)
        for child in self.children:
            child.print_tree(level + 1)

    def name(self):
        """Return the name of the file or directory."""
        return self.name

    def get_size(self):
        """Return the size of the file in bytes."""
        if self.size is None:
            try:
                self.size = os.path.getsize(self.path)
            except FileNotFoundError:
                self.size = 0
        return self.size

    def creation_date(self):
        """Return the creation date of the file."""
        return datetime.fromtimestamp(os.path.getctime(self.path))

    def modification_date(self):
        """Return the modification date of the file."""
        return datetime.fromtimestamp(os.path.getmtime(self.path))

    def delete(self):
        """Delete the file or directory."""
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)
        if self.parent:
            self.parent.children.remove(self)
        self.cache.remove(self.path)

    def change_permissions(self, mode):
        """Change the permissions of the file."""
        os.chmod(self.path, mode)

    def is_invisible(self):
        """Check if the file is hidden."""
        return self.name.startswith('.')

    def move(self, dst: str):
        try:
            # Try using shutil.move first
            shutil.move(self.path, dst)
            self._move_update_metadata(dst)
        except Exception as e:
            print(f"shutil.move failed: {e}")
            # If shutil.move fails, manually copy and then delete
            try:
                shutil.copy2(self.path, dst)  # copy2 preserves metadata
                os.remove(self.path)
                self._move_update_metadata(dst)
            except Exception as e:
                print(f"Manual copy and delete failed: {e}")

    def _move_update_metadata(self, new_path):
        # update paths
        self.revert_path = self.path
        self.path = new_path
        # update data structure
        self.parent.remove_child(self)
        self.parent = self.cache[os.path.dirname(new_path)]
        self.parent.add_child(self)
        # update cache
        self.cache.remove(self.revert_path)
        self.cache.update(new_path, self)

    def to_json(self):
        return {
            'path': self.path,
            'revert_path': self.revert_path,
            'cache_timestamp': self.cache_timestamp,
            'cache': self.cache,
            'parent': self.parent,
            'self.children': self.children
        }

    def get_hashed_value(self):
        """
        Hashes the contents of a file using SHA-256 and returns the hash in hexadecimal format.

        Parameters:
        - filepath: Path to the file to be hashed.

        Returns:
        - A hexadecimal string representation of the hash of the file's contents.
        """
        sha256_hash = hashlib.sha256()

        try:
            if os.path.isdir(self.path):
                return None
            else:
                # open file
                with open(self.path, "rb") as f:
                    # read contents in chunks to avoid memory issues
                    for byte_block in iter(lambda: f.read(4096), b""):
                        # update hashed value with each chunk
                        sha256_hash.update(byte_block)
                # return in hexadecimal format
                return sha256_hash.hexdigest()
        except FileNotFoundError:
            print(f"File not found: {self.path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def search(self, search_term: str):
        """Search for nodes including search_term as a substring in cache"""
        search_term = search_term.lower()  # Ensure case-insensitive comparison
        result_list = []

        for keyword, nodes in self.cache.keyword_index.items():
            if search_term in keyword:
                print(f"Keyword found: {keyword}")
                result_list.extend(nodes)  # Add all nodes associated with the found keyword

        if result_list:
            return result_list
        else:
            print("Keyword not found")
            return []

    def isinstance(self, obj_type: object):
        """Check if the node is an instance of the given type."""
        return isinstance(self.__class__, obj_type)

    def __str__(self):
        return self.name


class File(FileSystemNode):
    def __init__(self, path: str, cache: FileSystemCache, name, parent, size=None):
        super().__init__(path, cache, parent, size)
        self.name = name  # give file a name

    def __str__(self) -> str:
        return self.name

    def extension(self):
        """Return the file's extension."""
        _, ext = os.path.splitext(self.path)
        return ext


class Directory(FileSystemNode):
    """Represents a directory in the file system."""

    def __init__(self, path: str, cacheObj: FileSystemCache, name, parent):
        super().__init__(path, cacheObj, parent, size=None)
        self.name = name
        self._populate()  # Populate the directory with its children
        cacheObj.save_to_file()

    def _populate(self):
        """Populate the directory with its children and calculate directory size."""
        total_size = 0
        print(f"Populating directory {self.path}\nParent: {self.parent}")
        try:
            with os.scandir(self.path) as entries:
                for entry in entries:
                    print(f"Found entry: {entry.path}")
                    if entry.is_dir():
                        # Skip python version directories and hidden folders
                        if '.' in entry.name or entry.name.startswith('$'):
                            continue
                        child = Directory(entry.path, self.cache, name=entry.name, parent=self)
                        print(f"Created Directory: {child.path} with parent: {child.parent.path}")
                    else:
                        # Calculate file size and update total size for the directory
                        file_size = entry.stat().st_size
                        total_size += file_size
                        if entry.path.endswith(".wav") or entry.path.endswith(".aac") or entry.path.endswith(".mp3"):
                            child = Music(entry.path, self.cache, name=entry.name, parent=self, size=file_size)
                        elif entry.path.endswith(".jpeg") or entry.path.endswith(".jpg") or entry.path.endswith(".HEIC"):
                            # child = Image(entry.path, self.cache, name=entry.name, parent=self, size=file_size)
                            #TODO Fix image usage, currently causing FileNotFound Error due to subprocessing of CLI util
                            child = File(entry.path, self.cache, name=entry.name, parent=self, size=file_size)
                        else:
                            child = File(entry.path, self.cache, name=entry.name, parent=self, size=file_size)
                        print(f"Created File: {child.path} with parent: {child.parent.path}")
                        self.cache.update(child.path, child)
                    self.add_child(child)

            # After iterating through all entries, set the directory's size
            self.size = total_size
            print(f"inserting directory: {self.path} to cache")
            self.cache.update(self.path, self)

        except FileNotFoundError:
            print(f"Directory not found: {self.path}")

    def _multithread_populate(self):
        thread_pool = QThreadPool.globalInstance()

        # define callback function to add children from threads
        def add_child(child):
            self.children.append(child)
            child.parent = self

        try:
            with os.scandir(self.path) as entries:
                for entry in entries:
                    task = ScanTask(entry, self.cache, add_child)
                    thread_pool.start(task)
        except FileNotFoundError:
            print(f"Directory not found: {self.path}")

    def add_child(self, child: object):
        """Add a child file or directory."""
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: object):
        """Remove a child file or directory."""
        self.children.remove(child)

    def list_contents(self):
        """List all files and folders in the directory."""
        return [child.name for child in self.children]

    def find_file(self, file_name: str):
        """Recursively find a file in the directory and its subdirectories."""
        for child in self.children:
            if child.name == file_name:
                return child
            if isinstance(child, Directory):
                found = child.find_file(file_name)
                if found:
                    return found
        return None

    def find_files_by_extension(self, extension: str):
        """Recursively find all files with a given extension in the directory and its subdirectories."""
        matching_files = []  # List of matching files
        for child in self.children:  # Iterate over the children
            if isinstance(child, File) and child.extension() == extension:
                matching_files.append(child)
                print(f"Found file: {child.name}")  # Print the file path
            elif isinstance(child, Directory):
                matching_files.extend(child.find_files_by_extension(extension))

        return matching_files

    def calculate_folder_size(self) -> list[FileSystemNode]:
        for child in self.children:
            child.get_size()
        return self.children



class ScanTask(QRunnable):
    def __init__(self, entry:os.DirEntry, cache, add_child_callback):
        super().__init__()
        self.entry = entry
        self.cache = cache
        self.add_child_callback = add_child_callback

    def run(self):
        if self.entry.is_dir():
            child = Directory(self.entry.path, self.cache)
        else:
            child = File(self.entry.path, self.cache)

        self.cache.update(child.path, child)
        self.add_child_callback(child)


class Image(File):

    def __init__(self, path: str, cache, name, parent, size=None):
        super().__init__(path, cache, name, parent, size)
        self._width = None
        self._height = None
        self._coords = None
        self._location = None
        self._populate_image_metadata()

    @property
    def width(self):
        """Return the width of the image."""
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self):
        """Return the height of the image."""
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def coords(self):
        """Return the location of the image."""
        return self._coords

    @coords.setter
    def coords(self, value: tuple):
        self._coords = value

    @property
    def location(self):
        """Return the location of the image."""
        return self._location

    @location.setter
    def location(self, value: tuple):
        self._location = value

    def _populate_image_metadata(self):
        """
        Populate the image metadata.
        """
        # If the image is HEIC, convert using pyheif
        if self.extension().lower() == '.heic':
            heif_file = pyheif.read(self.path)
            image = PIL.Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            # Optionally, convert to JPEG or another format here
            # e.g., image.save(self.path.replace('.HEIC', '.jpeg'), "JPEG")
            self._extract_metadata_from_pil_image(image)
        else:
            image = PIL.Image.open(self.path)
            self._extract_metadata_from_pil_image(image)

    def _extract_metadata_from_pil_image(self, image):
        # Extract metadata from the PIL Image object
        exif_data = {}
        if hasattr(image, '_getexif'):
            exif_info = image._getexif()
            if exif_info is not None:
                for tag, value in exif_info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value

        self.width = exif_data.get('ExifImageWidth', image.width)
        self.height = exif_data.get('ExifImageHeight', image.height)
        self.coords = self.convert_gps_data(exif_data['GPSInfo']) if 'GPSInfo' in exif_data else None
        self.location = self.get_location_by_country() if self.coords else None

    def _populate_jpeg_metadata(self):
        try:
            image = PIL.Image.open(self.path)

            # Attempt to extract EXIF data
            exif_data = {}
            if hasattr(image, '_getexif'):  # Check if the image has EXIF data
                exif_info = image._getexif()
                if exif_info is not None:
                    for tag, value in exif_info.items():
                        decoded = TAGS.get(tag, tag)
                        exif_data[decoded] = value

            self.width = exif_data['ExifImageWidth'] if 'ExifImageWidth' in exif_data else image.width
            self.height = exif_data['ExifImageHeight'] if 'ExifImageHeight' in exif_data else image.height
            self.coords = self.convert_gps_data(exif_data['GPSInfo']) if 'GPSInfo' in exif_data else None
            self.location = self.get_location_by_country() if self.coords else None
        except Exception as e:
            print(f"Failed to extract metadata from {self.path}. Error: {e}")

    def heic_to_pillow_format(self):
        """
        Creates jpeg version of HEIC file in order to extract metadata using pillow library

        params:
        - heic_path: Path to the HEIC file.
        """
        try:
            subprocess.run(['heif-convert', self.path, self.path.split('.')[0]+'.jpeg'], check=True)
            self.path = self.path.split('.')[0]+'.jpeg'
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {self.path} to JPEG. Error: {e}")

    def get_location_by_country(self):
        """
        Get the location of the image by country using proximity logic.

        Parameters:
        - latitude: The latitude of the image.
        - longitude: The longitude of the image.

        Returns:
        The country of the image.
        """
        latitude, longitude = self.coords

        # Load the countries data
        countries = pd.read_csv('../../resources/country-coord.csv')

        # Apply the Haversine formula to each country's coordinates
        countries['Distance'] = countries.apply(
            lambda row: Image.haversine(latitude, longitude, row['Latitude (average)'],
                                                 row['Longitude (average)']), axis=1)

        # Find the country with the minimum distance to the given coordinates
        nearest_country = countries.loc[countries['Distance'].idxmin()]

        if not nearest_country.empty:
            return nearest_country['Country']
        else:
            return "No country found for these coordinates."


    @staticmethod
    def dms_to_decimal(degrees, minutes, seconds, direction):
        """
        Converts degrees, minutes, and seconds to decimal degrees.

        Parameters:
        - degrees, minutes, seconds: The parts of the DMS value.
        - direction: The compass direction ('N', 'S', 'E', 'W').

        Returns:
        The decimal degree representation.
        """
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if direction in ['S', 'W']:
            decimal = -decimal
        return decimal

    @staticmethod
    def convert_gps_data(gps_data: dict) -> tuple:
        """
        Converts GPS data from EXIF format to readable latitude and longitude.

        Parameters:
        - gps_data: A dictionary containing GPS data in EXIF format.

        Returns:
        A tuple containing (latitude, longitude) in decimal degrees.
        """
        latitude_dms = gps_data.get(2)
        latitude_direction = gps_data.get(1)
        longitude_dms = gps_data.get(4)
        longitude_direction = gps_data.get(3)

        if latitude_dms and latitude_direction and longitude_dms and longitude_direction:
            latitude = Image.dms_to_decimal(latitude_dms[0], latitude_dms[1], latitude_dms[2], latitude_direction)
            longitude = Image.dms_to_decimal(longitude_dms[0], longitude_dms[1], longitude_dms[2], longitude_direction)
            return latitude, longitude
        else:
            return None

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees).
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r


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

    def __init__(self, path: str, cache, name, parent, size=None):
        super().__init__(path, cache, name, parent, size)  # Call the constructor of the parent class
        self._artist = None  # Initialize artist attribute
        self._track_name = None  # Initialize track name attribute
        self._album = None # Initialize album attribute
        self._year = None  # Initialize year attribute
        self.get_music_data()

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

    def get_music_data(self) -> None:
        """
        Method to retrieve metadata from audio files.

        @return
        list[Music]: List of Music objects containing metadata
        """

        try:
            audio = EasyID3(self.path)  # Read ID3 tags from audio file
            if audio:
                # Extract metadata from ID3 tags
                self._artist = audio['artist'][0] if 'artist' in audio else None
                self._album = audio['album'][0] if 'album' in audio else None
                self._track_name = audio['title'][0] if 'title' in audio else None
                self._year = audio['year'][0] if 'year' in audio else None
            else:
                print(f"No metadata found in the file: {self.path}")
        except Exception as e:
            print(f"Error processing file {self.path}: {e}")

    def organize_music(self):
        """
        Method to organize music files into directories based on metadata.

        @params
        organize_by: str: criteria for organizing (artist, album, year)
        """
        if self.artist == None:
            print("No artist metadata found.")
            return

        parent_directory = os.path.dirname(self.path)
        target_directory = os.path.join(parent_directory, self.artist)  # Target directory based on artist
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)
            music_folder = Directory(target_directory, self.cache, 'Music', self.parent)
            # update attributes
            self.parent.add_child(music_folder)

        # keep track of original path to revert changes
        revert_path = self.revert_path
        self.move(target_directory+'/'+self.name)
        self.revert_path = revert_path
        print(f"Moved {self.path} to {target_directory}")


