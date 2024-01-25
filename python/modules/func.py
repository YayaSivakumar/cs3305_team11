# script name: func.py
import os, datetime, shutil, json

def get_all_file_paths(path: str) -> list[str]:
    """
    Function to get the paths of all files in path, disregarding parent directory.

    @params
    path: str: absolute path of directory to be traversed
    ret: list[str]: list of absolute paths
    """
    files_list = []
    # walk through all of the files in the specified path
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

def size_convert(size: int) -> str:
    """
    function to convert bytes to kilobytes

    @params
    size: int: size in bytes
    ret: str: size in kilobytes
    """
    try:
        return str(round(size/1000, 2)) + ' KB'
    except TypeError as e:
        raise TypeError(f"Error: {e}")

def time_convert(timestamp: int) -> str:
    """
    function to convert time to a readable format

    @params
    time: int: time in seconds
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

def save_to_json(file_list: list, json_file_path: str):
    """
    function to save the original structure to a JSON file

    @params
    md_list: list: list of file with metadata attributes
    json_file_path: str: path to JSON file
    """
    with open(json_file_path, 'w') as json_file:
        file_info = {}
        for file in file_list:
            file_info[file.path] = file.to_dict()
        json.dump(file_info, json_file)

def revert_changes(json_file_path: str):
    """
    function to revert changes made by organise_by_date_func

    @params
    json_file_path: str: path to JSON file containing original structure
    """
    with open(json_file_path, 'r') as json_file:
        files = json.load(json_file)

    for file, data in files.items():
        original_path = data['original_path']
        current_path = data['new_path']
        if os.path.exists(current_path) and not os.path.exists(original_path):
            move_file(current_path, original_path)


class File:
    def __init__(self, path, filetype):
        self._original_path = path
        self._filetype = filetype
        self._new_path = ''
        self._size = ''
        self._creation_time = ''
        self._modification_time = ''
        self._last_access_time = ''

    def to_dict(self):
        return {'original_path': self.original_path, 'new_path': self.new_path, 'filetype': self.filetype, 'size': self.size, 'creation_time': self.creation_time, 'modification_time': self._modification_time, 'last_access_time': self._last_access_time}
    
    @staticmethod
    def from_dict(my_dict: dict[str:str]):
        return File(my_dict['path'], my_dict['filetype'])

    @property
    def filetype(self) -> str:
        return self._filetype
    @filetype.setter
    def filetype(self, f:str) -> None:
        self._filetype = f
    @property
    def original_path(self) -> str:
        return self._original_path
    @original_path.setter
    def path(self, p) -> None:
        self._original_path = p
    @property
    def new_path(self) -> str:
        return self._new_path
    @new_path.setter
    def new_path(self, np: str) -> None:
        self._new_path = np
    @property
    def size(self) -> str:
        return self._size
    @size.setter
    def size(self, s: str) -> None:
        self._size = s
    @property
    def creation_time(self) -> str:
        return self._creation_time
    @creation_time.setter
    def creation_time(self, ct: str) -> str:
        self._creation_time = ct