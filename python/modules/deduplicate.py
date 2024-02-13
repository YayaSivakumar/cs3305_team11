# script_name: deduplicate.py
from python.model.FileSystemNodeModel import Directory, FileSystemCache
from python.modules.helper_funcs import delete_empty_directories


def deduplicate(dir_node: Directory):
    """
    Recursive function to delete duplicate files in the directory tree.
    """

    # set to store hashed values of files
    seen = set()

    deleted_files = _deduplicate(dir_node, seen)

    # delete empty directories if any after deduplication
    delete_empty_directories(dir_node, dir_node)

    return deleted_files

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
            deleted.append(child.path)
            child.delete()

        # add hash if child is a File Object
        elif hashed_value:
            seen.add(hashed_value)

    print(f"Deleted: {deleted}")
    return deleted

if __name__ == "__main__":
    '''
    c = FileSystemCache()
    dir_node = Directory('/Users/yachitrasivakumar/Downloads', c)
    c.save_to_file()
    deleted = deduplicate(dir_node)
    '''
    pass