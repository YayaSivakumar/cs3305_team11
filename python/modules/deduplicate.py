# script_name: deduplicate.py
from python.model.FileSystemNodeModel import Directory

def deduplicate(dir_node: Directory):
    """
    Recursive function to delete duplicate files in the directory tree.
    """
    # set to store hashed values of files
    seen = set()

    duplicate_files = _deduplicate(dir_node, seen)

    return duplicate_files


def _deduplicate(dir_node: Directory, seen: set):
    deleted = []
    # work on a copy of children to safely modify the list during iteration
    for child in dir_node.children[:]:

        hashed_value = child.get_hashed_value()

        # if the child is a directory, recursively process it
        if isinstance(child, Directory):
            _deduplicate(child, seen)

        # if the child has been seen before, delete it
        if hashed_value in seen and not child.is_invisible():
            deleted.append(child)

        # add hash if child is a File Object
        elif hashed_value:
            seen.add(hashed_value)

    return deleted


if __name__ == "__main__":
    pass