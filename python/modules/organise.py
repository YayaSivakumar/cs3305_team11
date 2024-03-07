from python.modules.organise_by_date import organise_by_date
from python.modules.organise_by_type import organise_by_type_func
from python.model.FileSystemNodeModel import Directory
from python.model.Music import Music


def organise(dir_node: Directory):

    # sort initial files by type
    organise_by_type_func(dir_node)

    # sort music by artist
    sort_music(dir_node)

    # sort images by date
    sort_images(dir_node)


def sort_images(dir_node: Directory):
    if dir_node.path + '/Photos' in dir_node.cache.keys():
        image_folder_node = dir_node.cache[dir_node.path + '/Photos']
        organise_by_date(image_folder_node)


def sort_music(dir_node: Directory):
    if dir_node.path + '/Music' in dir_node.cache.keys():
        music_folder_node = dir_node.cache[dir_node.path + '/Music']
        for file in music_folder_node.children[:]:
            if type(file) == Directory:
                continue
            file.organize_music()
