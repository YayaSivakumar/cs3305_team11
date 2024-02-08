from __future__ import annotations
import shutil
import os 
import eyed3
from helper_funcs import *


class MusicFile:
    def __init__(self, path: str, artist:str, track_name:str, album:str, year:int):
        self.path = path
        self.artist = artist
        self.track_name = track_name
        self.album = album
        self.year = year



    def __repr__(self):
        return f"MusicFile(path={self.path}, artist={self.artist}, track_name={self.track_name}, album={self.album}, year={self.year})"



def get_music_data(path):
    music_files = []
    file_paths = get_all_file_paths(path)
    for file in file_paths:
        extension = file.split('.')[-1]
        if extension in ['wav', 'mp3', 'aac', 'm4a']:
            try:
                audio = eyed3.load(file)
                if audio.tag is not None:
                    music_files.append(MusicFile(
                        path=file,
                        artist=audio.tag.artist,
                        track_name=audio.tag.title,
                        album=audio.tag.album,
                        year=int(audio.tag.recording_date) if audio.tag.recording_date else None

                    ))
                else:
                    print(f"No metadata data found in the file: {file}")
            except eyed3.id3.tag.TagException as e:
                print(f"Error processing file {file}: {e}")

    return music_files

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def organise_by_artist(files):
    for file in files:
        artist_directory = os.path.join(music_directory, file.artist)
        create_directory(artist_directory)

        shutil.move(file.path, os.path.join(artist_directory, os.path.basename(file.path)))

music_directory = "C:/Users/evely/OneDrive/Documents/Testing files/test music"

music_files = get_music_data(music_directory)
# organise_by_artist(music_files)

def organise_by_album(files):
    for file in files:
        album_directory = os.path.join(music_directory, file.album)
        create_directory(album_directory)

        shutil.move(file.path, os.path.join(album_directory, os.path.basename(file.path)))

# organise_by_album(music_files)

def organise_by_song_year(files):
    for file in files:
        song_year_directory = os.path.join(music_directory, file.year)
        create_directory(song_year_directory)

        shutil.move(file.path, os.path.join(song_year_directory, os.path.basename(file.path)))

organise_by_song_year(music_files)
