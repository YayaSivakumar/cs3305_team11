# script name: organise_by_date.py
import os
from python.model.FileSystemNodeModel import Directory


def organise_by_date(dir_node: Directory):
    """
    main function for organise by date function.

    @params
    path_to_organise: str: absolute path to directory to be organised
    dir_traversal_type: function: name of function to be used to traverse the directory
    """

    # create the required directories and move the files
    _organise_by_date(dir_node)


def _organise_by_date(dir_node: Directory):
    """
    function to create the required directories

    @params
    filepath: str: path to create directories at
    required: list[str]: list of the required folders
    """
    month_names = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                   '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

    # create copy of child list to avoid changing the list while iterating
    for node in dir_node.children[:]:

        if isinstance(node, Directory):
            continue

        if not node.is_invisible():

            # extract year and month from modification date
            print(node.path, node.creation_date())
            year = str(node.creation_date()).split('-')[0]
            month = month_names[str(node.creation_date()).split('-')[1]]

            # create directories if they don't already exist
            if year not in os.listdir(dir_node.path):
                os.makedirs(dir_node.path + '/' + year)
                dir_node.add_child(Directory(dir_node.path + '/' + year, dir_node.cache, year, dir_node))
            if month not in os.listdir(dir_node.path + '/' + year):
                os.makedirs(dir_node.path + '/' + year + '/' + month)
                year_node = dir_node.find_node_from_cache(dir_node.path + '/' + year)
                year_node.add_child(
                    Directory(dir_node.path + '/' + year + '/' + month, dir_node.cache, month, dir_node))

            # move item to the correct directory
            new_file_path = os.path.join(dir_node.path + '/' + year + '/' + month + '/' + node.name)

            # keep track of original path to revert changes
            revert_path = node.revert_path
            node.move(new_file_path)
            node.revert_path = revert_path


if __name__ == "__main__":
    pass
