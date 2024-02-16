# script name: organise_photos_by_location.py
from python.model.FileSystemNodeModel import *
from python.model.FileSystemCache import FileSystemCache
from python.model.Image import Image
import os


def organise_photos_by_location(dir_node: Directory) -> None:
    """
    function to organise photos by location

    @params
    file_path: str: absolute path to photo file
    """
    for child_node in dir_node.children[:]:
        print(child_node.path)
        if type(child_node) == Image:

            print(child_node.path, child_node.location)

            # get location attributes if not None
            if child_node.location:

                # create folder for location if it doesn't exist
                location = dir_node.find_node(child_node.location)
                if not location:
                    os.makedirs(dir_node.path + '/' + child_node.location)
                    location = Directory(dir_node.path + '/' + child_node.location, dir_node.cache)
                    dir_node.add_child(location)

                # move photo to location folder
                child_node.move(dir_node.path + '/' + location + '/' + child_node.name)

    return None


if __name__ == '__main__':
    pass

