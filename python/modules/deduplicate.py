# script_name: deduplicate.py
from python.model.FileSystemNodeModel import Directory


def deduplicate(dir_node: Directory):
    """
    Recursive function to delete duplicate files in the directory tree.
    """
    # set to store hashed values of files
    seen = set()

    # recursively delete duplicate files
    duplicate_files = _deduplicate(dir_node, seen)

    return duplicate_files


def _deduplicate(dir_node: Directory, seen: set, deleted: list = []):
    """
    Recursive function to delete duplicate files in the directory tree.

    @params
    dir_node: Directory: directory node to be deduplicated
    seen: set: set to store hashed values of files
    deleted: list: list to store deleted files
    """

    # work on a copy of children to safely modify the list during iteration
    for child in dir_node.children[:]:
        # get the hashed value of the child
        hashed_value = child.get_hashed_value()
        print(hashed_value, seen)

        # if the child is a directory, recursively process it
        if isinstance(child, Directory):
            _deduplicate(child, seen, deleted)

        # if the child has been seen before, delete it
        elif hashed_value in seen and not child.is_invisible():
            deleted.append(child)

        # add hash if child is a File Object
        else:
            seen.add(hashed_value)

    return deleted


if __name__ == "__main__":
    pass