# script name: organise_photos_by_location.py
from python.model.FileSystemNodeModel import Directory
from python.model.Image import Image

def organise_photos_by_location(dir_node: Directory) -> None:
    """
    function to organise photos by location

    @params
    file_path: str: absolute path to photo file
    """
    for node in dir_node.children[:]:

        if node.isinstance(Image):
            # get location attributes

            # create folder for location if it doesn't exist

            # move photo to location folder
            pass

