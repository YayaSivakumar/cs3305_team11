# script name: func.py
import os, datetime

def get_file_paths(path):
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