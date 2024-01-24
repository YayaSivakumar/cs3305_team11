# script name: sort.py
import os
import shutil
from func import get_file_paths
FILEPATH_TEST = '/Users/jackmoloney/Developer/cs3305_team11/Tester'

def main_func(path_to_organise: str):
    file_paths = get_file_paths(path_to_organise) # array of file paths
    file_obj_array: list[File] = []
    directories_to_create: set[str] = set()
    for file in file_paths:
        # get filetype
        filetype = determine_filetype(file)
        # if filetype not already in list of directories to create, add it
        if filetype not in directories_to_create:
            directories_to_create.add(filetype)
        temp = File(file, filetype)
        file_obj_array.append(temp)

    # Folder names are defined here, pending later feature addition
    folder_names = {'documents': 'Documents', 'photos': 'Photos', 'videos':'Videos', 'music':'Music', 'misc':'Misc'}
    create_target_directories(path_to_organise, list(directories_to_create), folder_names) # create necessary directories
    num_files_moved = 0
    # move files to appropriate target
    for file_obj in file_obj_array:
        source = file_obj.path
        destination = path_to_organise+ '/' + folder_names[file_obj.filetype]
        move_file(source, destination)
        num_files_moved += 1
    print(f'Moved {num_files_moved} files')



def move_file(source: str, dest: str):
    try:
        shutil.move(source, dest)
    except IOError as e:
        print(f"Error: {e}")

def determine_filetype(filename: str) -> str:
    """
    function to determine what type a file is based on the filename

    @params
    filename: Name of file to be checked
    ret: file type based on categories returned as a string
    """
    extension = filename.split('.')[-1]
    # print(f"ext: {extension}")
    types = {'documents':['pdf', 'docx', 'doc', 'txt', 'text'], \
             'photos':['jpeg', 'jpg', 'svg', 'png', 'PNG'],\
             'videos': ['mp4', 'mov', 'avi'],\
             'music': ['wav', 'mp3', 'aac']}
    
    for category in types:
        if extension in types[category]:
            return category
        

    return 'misc'

def create_target_directories(filepath: str, required: list[str], folder_names: dict[str:str]):
    """

    @params
    filepath: str: path to create directories at
    required: list[str]: list of the required folders
    """
    contents = list_dir(filepath) # return [str] of files/directories
    for i in required:
        directory = folder_names[i] 
        if directory not in contents:
            os.makedirs(filepath+'/'+directory)
    

def get_pwd():
    return os.getcwd()

def list_dir(filepath: str) -> str:
    return os.listdir(filepath)


class File:
    def __init__(self, path, filetype):
        self._path = path
        self._filetype = filetype
    
    @property
    def filetype(self) -> str:
        return self._filetype
    @filetype.setter
    def filetype(self, f):
        self._filetype = f
    @property
    def path(self) -> str:
        return self._path
    @path.setter
    def path(self, p):
        self._path = p
    
    
if __name__ == "__main__":
    main_func(FILEPATH_TEST)