# script name: sort.py
import os
import shutil
FILEPATH_TEST = '/User/jackmoloney/Developer/cs3305_team11/Tester'

def main(path_to_organise):
    file_paths = get_file_paths(path_to_organise) # array of file paths
    file_obj_array: [File] = []
    directories_to_create = set()
    for file in file_paths:
        # get filetype
        filetype = determine_filetype(file)
        # if filetype not already in list of directories to create, add it
        if filetype not in directories_to_create:
            directories_to_create.add(filetype)
        temp = File(file, filetype)
        file_obj_array.append(temp)

    # Folder names are defined here, pending later feature addition
    folder_names = {'documents': 'Documents', 'photos': 'Photos', 'videos':'Videos', 'music':'Music'}
    create_target_directories(path_to_organise, list(directories_to_create), folder_names) # create necessary directories
    num_files_moved = 0
    # move files to appropriate target
    for file_obj in file_obj_array:
        source = file_obj.path
        destination = path_to_organise + folder_names[file.type]
        move_file(source, destination)
        num_files_moved += 1
    print(f'Moved {num_files_moved} files')



def move_file(source: str, dest: str):
    try:
        shutil.move(source, dest, )
    except IOError as e:
        print(f"Error: {e}")

def get_file_paths(path):
    files_list = []
    # walk through all of the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list

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
    for dir in required:
        if dir not in contents:
            os.makedirs(filepath+'/'+dir)
    

def get_pwd():
    return os.getcwd()

def list_dir(filepath: str) -> str:
    return os.listdir(filepath)


class File:
    def __init__(self, path, filetype):
        self.path = path
        self.filetype = filetype
    
    @property
    def filetype(self):
        return self.filetype
    @property
    def path(self):
        return self.path
    
if __name__ == "__main__":
    main(FILEPATH_TEST)