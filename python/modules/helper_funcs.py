# script name: helper_funcs.py
from __future__ import annotations
import datetime
from python.model.FileSystemNodeModel import Directory


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


def delete_empty_directories(dir_node: Directory, root: Directory):
    """
    Recursive function to delete empty directories in the directory tree.

    @params
    dir_node: Directory: directory to be checked for empty subdirectories
    root: Directory: root directory of the tree
    """

    # work on a copy of children to safely modify the list during iteration
    for child in dir_node.children[:]:

        if isinstance(child, Directory):

            # recursively process child directories
            delete_empty_directories(child, root)

            # check if the child directory is now empty and child has not been deleted
            if not child.children and child.cache.get(child.path):
                child.delete()

        elif child.is_invisible():
            child.delete()

    # check if the current directory is now empty and not the root
    if not dir_node.children and dir_node != root:
        dir_node.delete()


if __name__ == "__main__":
    pass
