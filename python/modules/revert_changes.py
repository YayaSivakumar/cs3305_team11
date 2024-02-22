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
            print(node.name, node.path, node.revert_path)
            # move file back to original location
            node.move(node.revert_path)


if __name__ == "__main__":
    # testing
    '''
    cache = FileSystemCache()
    dir_obj = Directory('/Users/yachitrasivakumar/Desktop/YEAR3/Semester2Year3/cs3305_team11/test_by_date', cache)

    def print_contents(node: Directory):
        print(node.list_contents())
        for child in node.children:
            if isinstance(child, Directory):
                print_contents(child)

    organise_by_date(dir_obj)
    # check for data structure consistency
    print('after organising by date')
    print_contents(dir_obj)

    print('after reverting changes')
    revert_changes(dir_obj)
    # check for data structure consistency
    print_contents(dir_obj)
    '''

