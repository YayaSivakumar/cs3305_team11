# from __future__ import annotations
# import os
# from helper_funcs import time_convert, size_convert, get_all_file_paths, get_file_and_subdir_paths, move_file, save_to_json, File, revert_changes
import eyed3


def get_music_data(file):

    audio = eyed3.load(file)
    track_name = audio.tag.title
    artist = audio.tag.artist
    album = audio.tag.album
    year = audio.tag.year