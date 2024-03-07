# script name: revert_changes.py
from python.model.FileSystemNodeModel import Directory
from python.modules.helper_funcs import delete_empty_directories


def revert_changes(dir_node: Directory):
    try:
        _revert_changes(dir_node)

        # delete empty directories
        delete_empty_directories(dir_node)

    except FileNotFoundError as e:
        print(e)


def _revert_changes(dir_node: Directory):
    """
    function to revert changes and put files back in the original location

    @params
    json_file_path: str: path to JSON file containing original structure
    """

    # iterate through shallow copy of children list to avoid changing the list while iterating
    for node in dir_node.children[:]:

        # recursively revert changes for each file
        if isinstance(node, Directory):
            _revert_changes(node)

        if node.path != node.revert_path:
            # move file back to original location
            node.move(node.revert_path)


if __name__ == "__main__":
    pass

