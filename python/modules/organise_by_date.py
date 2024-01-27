from __future__ import annotations
import os
from python.modules.helper_funcs import time_convert, size_convert, get_all_file_paths, get_file_and_subdir_paths, move_file, save_to_json, File


def organise_by_date_func(path_to_organise: str, dir_traversal_type: function = get_all_file_paths):
    """
    main function for organise by date function.

    @params
    path_to_organise: str: absolute path to directory to be organised
    dir_traversal_type: function: name of function to be used to traverse the directory
    """

    # get metadata from each file in the directory
    md_list = get_metadata_from_files(dir_traversal_type(path_to_organise))
    # create the required directories and move the files
    organise_by_date(md_list, path_to_organise) 

    # Save the original structure to a JSON file
    save_to_json(md_list)


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


def get_metadata_from_files(filepath_list: list):
    """
    function to get the metadata from a file 

    @params
    filepath: str: absolute path to a file
    """
    md_list = []

    # get the time data from each file
    for filepath in filepath_list:

        stats = os.stat(filepath)
        
        file = File(filepath, filepath.split('.')[-1])
        file.size = size_convert(stats.st_size)
        file.creation_time = time_convert(stats.st_ctime)
        file.modification_time = time_convert(stats.st_mtime)
        file.last_access_time = time_convert(stats.st_atime)
        
        md_list.append(file)

    return md_list


def organise_by_date(md_list: list, directory_path: str):
    """
    function to create the required directories

    @params
    filepath: str: path to create directories at
    required: list[str]: list of the required folders
    """
    month_names = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June',\
                   '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
    
    # iterate through each file and obtain year and month of modification(/creation/last access)
    for file in md_list:
        # get list of directories already created in path
        list_of_directories = os.listdir(directory_path)
        # get year and month of modification
        year = file.creation_time.split('-')[0]
        m = file.creation_time.split('-')[1]
     
        month = month_names[m]  # for test purposes I am using the 'Modified Time' values

        # create directories if they don't already exist
        if year not in list_of_directories:
            os.makedirs(directory_path+'/'+year)
        if month not in os.listdir(directory_path+'/'+year):
            os.makedirs(directory_path+'/'+year+'/'+month)

        # move item to the correct directory
        move_file(file.original_path, directory_path+'/'+year+'/'+month)

        # update new path in metadata dictionary
        file.new_path = directory_path+'/'+year+'/'+month+'/'+(file.original_path.split('/'))[-1]


if __name__ == "__main__":
    pass
