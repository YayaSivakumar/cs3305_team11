# script name: organise_by_type.py
from python.model.FileSystemNodeModel import *
from python.model.FileSystemCache import FileSystemCache
import os


def organise_by_type_func(dir_path: str):
    """
    Main function for organise by filetype feature. Takes a file path and breaks every file in that directory
    and its subdirectories

    @params
    path_to_organise: str: absolute path of folder to be organised
    folder_names: dict[str:str]: dictionary containing k,v pairs of file classification and the name of folder it will be placed in.
    ret: None
    """
    dir_node = Directory(dir_path, FileSystemCache())
    # determine different file types present, create list of needed directories
    created_directories = set()
    num_files_moved = 0

    # iterate through children
    for file_node in dir_node.children[:]:

        if type(file_node) == File:

            # get filetype
            filetype = determine_filetype(file_node)

            # if filetype directory not already created, create it
            if filetype not in created_directories:
                # create directory
                os.makedirs(dir_node.path + '/' + filetype)
                new_dir = Directory(dir_node.path + '/' + filetype, dir_node.cache)
                # update attributes
                dir_node.add_child(new_dir)
                created_directories.add(filetype)

            # move file to appropriate directory
            file_node.move(dir_node.path + '/' + filetype + '/' + file_node.name)
            num_files_moved += 1

    return f'Moved {num_files_moved} files'


def determine_filetype(file_node: File) -> str:
    """
    function to determine what type a file is based on the filename

    @params
    filename: Name of file to be checked
    ret: file type based on categories returned as a string
    """

    types = {'Documents': ['.pdf', '.docx', '.doc', '.txt', '.text'],
             'Photos': ['.jpeg', '.jpg', '.svg', '.png', '.PNG'],
             'Videos': ['.mp4', '.mov', '.avi'],
             'Music': ['.wav', '.mp3', '.aac']}

    extension = file_node.extension()
    for category in types:
        if extension in types[category]:
            return category

    return 'Misc'


if __name__ == "__main__":
    organise_by_type_func(input())
