# script name: helper_funcs.py
from __future__ import annotations
import datetime
import json
import os
import shutil


def get_all_file_paths(path: str) -> list[str]:
    """
    Function to get the paths of all files in path, disregarding parent directory.

    @params
    path: str: absolute path of directory to be traversed
    ret: list[str]: list of absolute paths
    """
    files_list = []
    # walk through all the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list


def get_file_and_subdir_paths(path: str):
    """
    Function to get the paths of files and immediate subdirectories in a directory.

    Treats subdirectories as a unit, does not enter the subdir.

    @params
    path: str: path to root directory

    ret: list[str]: list of paths to all files and immediate subdirectories
    """
    files_list = []
    # List all entries in the given directory
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        # Check if the entry is a file or a directory (but don't recurse into subdirectories)
        if os.path.isfile(full_path) or os.path.isdir(full_path):
            files_list.append(full_path)

    return files_list


def size_convert(size: int | float) -> str:
    """
    function to convert bytes to kilobytes

    @params
    size: int: size in bytes
    ret: str: size in kilobytes
    """
    try:
        return str(round(size / 1000, 2)) + ' KB'
    except TypeError as e:
        raise TypeError(f"Error: {e}")


def time_convert(timestamp: int | float) -> str:
    """
    function to convert time to a readable format

    @params
    timestamp: int: time in seconds
    ret: str: time in readable format
    """
    try:
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except TypeError as e:
        raise TypeError(f"Error: {e}")


def move_file(source: str, dest: str):
    """
    function to move file using shutil move

    @params
    source: str: absolute path to source file
    dest: str: absolute path to destination
    """
    try:
        shutil.move(source, dest)
    except IOError as e:
        print(f"Error: {e}")


def create_list_of_file_obj(file_dict: dict):
    file_list = []
    for key, values in file_dict.items():
        file = File.from_dict(values)
        file_list.append(file)
    return file_list


def save_to_json(file_list: list[File], json_file_path: str = 'cache/file_data.json'):
    """
    function to save the original structure to a JSON file

    @params
    md_list: list: list of file with metadata attributes
    json_file_path: str: path to JSON file
    """
    if not os.path.exists(json_file_path):
        # code to create file here
        os.makedirs('cache', exist_ok=True)

    with open(json_file_path, 'w') as json_file:
        file_info = {}
        for file in file_list:
            file_info[file.original_path] = file.to_dict()
        json.dump(file_info, json_file)


def load_json(json_file_path: str | bytes) -> dict:
    """
    function to load a json to a Python dictionary object.

    @params
    json_file_path: str|bytes: either json file or path to json file to be loaded
    ret: dict: dictionary representation of json file
    """
    with open(json_file_path, 'r') as json_file:
        ret = json.load(json_file)
    return ret


class File:
    """
    Represents an abstract file with metadata including paths, type, and timestamps.

    This class encapsulates details such as the file's original and new paths, type, size,
    and timestamps related to its creation, last modification, and last access.

    Attributes:
        _original_path (str): The original filesystem path of the file.
        _file_name (str): The name of the file extracted from the original path.
        _filetype (str): The type or extension of the file.
        _current_path (str): The new or updated filesystem path of the file, if any.
        _size (str): The size of the file.
        _creation_time (str): The timestamp of when the file was created.
        _modification_time (str): The timestamp of the last modification to the file.
        _last_access_time (str): The timestamp of the last access to the file.
    """

    def __init__(self, path: str, filetype: str):
        """
        Initializes a new instance of the File class with the specified path and filetype.

        @params:
        path: str: The full path to the file.
        filetype: str: The type or extension of the file.
        """
        self._original_path = path
        self._file_name = self._original_path.split('/')[-1]
        self._filetype = filetype
        self._current_path = ''
        self._size = ''
        self._creation_time = ''
        self._modification_time = ''
        self._last_access_time = ''

    def to_dict(self) -> dict:
        """
        Converts the File object to a dictionary with its metadata.

        Returns:
            dict: A dictionary representation of the File object including all metadata.
        """
        return {
            'original_path': self._original_path,
            'current_path': self._current_path,
            'filetype': self._filetype,
            'size': self._size,
            'creation_time': self._creation_time,
            'modification_time': self._modification_time,
            'last_access_time': self._last_access_time
        }

    @staticmethod
    def from_dict(my_dict: dict) -> 'File':
        """
        Creates a File object from a dictionary containing file metadata.

        Args:
            my_dict (dict): A dictionary with keys corresponding to the File object's attributes.

        Returns:
            File: A new File object initialized with the metadata from the dictionary.
        """
        file_from_dict = File(my_dict['original_path'], my_dict['filetype'])
        file_from_dict.current_path = my_dict['current_path']
        file_from_dict.size = my_dict['size']
        file_from_dict.creation_time = my_dict['creation_time']
        file_from_dict.modification_time = my_dict['modification_time']
        file_from_dict.last_access_time = my_dict['last_access_time']
        return file_from_dict

    @property
    def filetype(self) -> str:
        """The filetype or extension of the file."""
        return self._filetype

    @filetype.setter
    def filetype(self, f: str) -> None:
        self._filetype = f

    @property
    def original_path(self) -> str:
        """The original filesystem path of the file."""
        return self._original_path

    @original_path.setter
    def original_path(self, p: str) -> None:
        self._original_path = p

    @property
    def current_path(self) -> str:
        """The new or updated filesystem path of the file, if any."""
        return self._current_path

    @current_path.setter
    def current_path(self, np: str) -> None:
        self._current_path = np

    @property
    def size(self) -> str:
        """The size of the file."""
        return self._size

    @size.setter
    def size(self, s: str) -> None:
        self._size = s

    @property
    def creation_time(self) -> str:
        """The timestamp of when the file was created."""
        return self._creation_time

    @creation_time.setter
    def creation_time(self, ct: str) -> None:
        self._creation_time = ct

    @property
    def modification_time(self) -> str:
        """The timestamp of the last modification to the file."""
        return self._modification_time

    @modification_time.setter
    def modification_time(self, mt: str) -> None:
        self._modification_time = mt

    @property
    def last_access_time(self) -> str:
        """The timestamp of the last access to the file."""
        return self._last_access_time

    @last_access_time.setter
    def last_access_time(self, lat: str) -> None:
        self._last_access_time = lat

class PDF:

    def __init__(self, title: str, authors: list, date: str):
        self._title = title
        self._authors = authors
        self._creation_date = date

    def __str__(self):
        return f'Title: {self.title}\nAuthor: {self.authors}\nDate: {self.creation_date}\n'

    @property
    def title(self):
        return self._title

    @property
    def authors(self):
        return self._authors

    @property
    def creation_date(self):
        return self._creation_date

if __name__ == "__main__":
    pass