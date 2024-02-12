# script_name: deduplicate.py
from python.model.FileSystemNodeModel import Directory
from python.modules.helper_funcs import delete_empty_directories


def deduplicate(dir_node: Directory):
    """
    Recursive function to delete duplicate files in the directory tree.
    """

    # set to store hashed values of files
    seen = set()

    _deduplicate(dir_node, seen)

    # delete empty directories if any after deduplication
    delete_empty_directories(dir_node, dir_node)


def _deduplicate(dir_node: Directory, seen: set):

    # work on a copy of children to safely modify the list during iteration
    for child in dir_node.children[:]:

        hashed_value = child.get_hashed_value()

        # if the child is a directory, recursively process it
        if isinstance(child, Directory):
            _deduplicate(child, seen)

        # if the child has been seen before, delete it
        if hashed_value in seen:
            child.delete()

        # add hash if child is a File Object
        elif hashed_value:
            seen.add(hashed_value)


if __name__ == "__main__":
    pass