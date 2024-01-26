from __future__ import annotations
import os
from helper_funcs import time_convert, size_convert, get_all_file_paths, get_file_and_subdir_paths, move_file, save_to_json, File, revert_changes

import eyed3

def get_music_data(file):
    audio = eyed3.load(file)
    if audio.tag is not None:
        track_name = audio.tag.title
        artist = audio.tag.artist
        album = audio.tag.album
        year = audio.tag.recording_date


        print(f"Title: {track_name}")
        print(f"Artist: {artist}")
        print(f"Album: {album}")
        print(f"Year: {year}")

    else:
        print("No metadata found in the file")    

mp3_file_path = "C:/Users/evely/OneDrive/Documents/Testing files/test music/Future Islands - Before the Bridge.mp3"
get_music_data(mp3_file_path)