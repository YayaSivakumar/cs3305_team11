# script name: func.py
import os

def get_file_paths(path):
    files_list = []
    # walk through all of the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list