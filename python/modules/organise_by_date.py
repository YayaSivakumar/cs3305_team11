import os
import shutil
import datetime

def main(path_to_organise):
    # get metadata from each file in the directory
    md_dict = get_metadata_from_files_and_dirs(get_item_paths(path_to_organise))
    # create the required directories and move the files
    organise_by_date(md_dict, path_to_organise)

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
    
def get_file_paths(path: str):
    """
    function to get the paths of all files in a directory
    
    @params
    path: str: path to root directory
    """
    files_list = []
    # walk through all of the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list

def get_item_paths(path: str):
    """
    Function to get the paths of all files and immediate subdirectories in a directory.

    @params
    path: str: path to root directory

    returns
    contents_list: list: list of paths to all files and immediate subdirectories
    """
    files_list = []
    # List all entries in the given directory
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        # Check if the entry is a file or a directory (but don't recurse into subdirectories)
        if os.path.isfile(full_path) or os.path.isdir(full_path):
            files_list.append(full_path)
    
    return files_list

def get_file_paths(path):
    """
    function to get the paths of all files in a directory
    
    @params
    path: str: path to root directory
    """
    files_list = []
    # walk through all of the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list

def get_metadata_from_files_and_dirs(filepath_list: list):
    """
    function to get the metadata from a file 

    @params
    filepath: str: absolute path to a file
    """

    md_dict = {}

    # get the time data from each file
    for filepath in filepath_list:

        stats = os.stat(filepath)
        
        attrs = {
            'Absolute Path': filepath,
            'File Type': filepath.split('.')[-1],
            'Size (KB)': size_convert(stats.st_size),
            'Creation Time': time_convert(stats.st_ctime),
            'Modified Time': time_convert(stats.st_mtime),
            'Last Access Time': time_convert(stats.st_atime),
        }
        
        md_dict[filepath] = attrs 

    return md_dict

def move_file(source: str, dest: str):
    try:
        shutil.move(source, dest)
    except IOError as e:
        print(f"Error: {e}")

def organise_by_date(md_dict: dict, directory_path: str):
    """
    function to create the required directories

    @params
    filepath: str: path to create directories at
    required: list[str]: list of the required folders
    """
    month_names = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June',\
                   '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
    
    # iterate through each file and obtain year and month of modification(/creation/last access)
    for key, values in md_dict.items():
        # get list of directories already created in path
        list_of_directories = os.listdir(directory_path)
        # get year and month of modification
        year = values['Creation Time'].split('-')[0] # the reason for using 'Modified Time' in this function is because the 'Creation Time' values changed when I moved them into test_by_date folder
        month = month_names[values['Creation Time'].split('-')[1]] # for test purposes I am using the 'Modified Time' values

        # create directories if they don't already exist
        if year not in list_of_directories:
            os.makedirs(directory_path+'/'+year)
        if month not in os.listdir(directory_path+'/'+year):
            os.makedirs(directory_path+'/'+year+'/'+month)

        # move item to the correct directory
        move_file(key, directory_path+'/'+year+'/'+month)

if __name__ == "__main__":
    main(os.getcwd()+'/test_by_date')