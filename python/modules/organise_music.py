from __future__ import annotations
import shutil
import os 
import eyed3
# import os
# # from helper_funcs import time_convert, size_convert, get_all_file_paths, get_file_and_subdir_paths, move_file, save_to_json, File, revert_changes
# from helper_funcs import *


# def get_music_data(path):
#     file_paths = get_all_file_paths(path)
#     for file in file_paths:

#         extension = file.split('.')[-1]
#         if extension == 'wav'or extension =='mp3'or extension == 'aac':
#             audio = eyed3.load(file)
#             if audio.tag is not None:
#                 music_dict = {
#                     'Title' : audio.tag.title,
#                     'Artist' :audio.tag.artist,
#                     'Album' : audio.tag.album,
#                     'Year' : audio.tag.recording_date
#                 }
#                 # music_dict={}
#                 # music_dict['track_name'] = audio.tag.title
#                 # music_dict['artist'] = audio.tag.artist
#                 # music_dict['album'] = audio.tag.album
#                 # music_dict['year'] = audio.tag.recording_date

                

#                 # print(f"Title: {track_name}")
#                 # print(f"Artist: {artist}")
#                 # print(f"Album: {album}")
#                 # print(f"Year: {year}")

#                 # return music_dict=
#                 print(music_dict)
#                 return music_dict

#             else:
#                 print("No metadata found in the file")    

# # mp3_file_path = "C:/Users/evely/OneDrive/Documents/Testing files/test music/Future Islands - Before the Bridge.mp3"
# # mp3_file_path = "C:\Users\evely\OneDrive\Documents\Testing files\127782.jpg"
# path = "C:/Users/evely/OneDrive/Documents/Testing files/test music"
# get_music_data(path)


# def organise_by_artist(path_to_organise):

#     music_file_object_array : list[MusicFile] = []
#     artist_directories_needed :set[str] = set()

#     #get all songs by artist 
#         #create directory of artist name
#         #go through either adding to dictionary or make new
    
#     #if artist doesn't exist add to misc 

#     for artist in music_dict.get(artist):
#         if artist not in artist_directories_needed:
#             artist_directories_needed.add(artist)
#         add = MusicFile(artist, )
#         music_file_object_array.append(add)

#     create_artist_directories()

# def create_artist_directories(filepath: str, required: list[str], folder_names: dict[str:str]):
#     contents = list_dir(filepath)
#     for i in required:
#         directory = folder_names[i]
#         if directory not in contents:
#             os.makedirs(filepath+'/'+directory)


# def list_dir(filepath: str) -> list[str]:
#     return os.listdir(filepath)



def get_all_file_paths(path: str) -> list[str]:
    """
    Function to get the paths of all files in path, disregarding parent directory.

    @params
    path: str: absolute path of directory to be traversed
    ret: list[str]: list of absolute paths
    """
    files_list = []
    # walk through all the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list

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

'''
### old music class ###
class MusicFile(File):
    
    def __init__(self, path: str, filetype:str , artist:str , track_name:str , album:str, year:int , runtime:float):
        super.__init__(path, filetype)
        self._artist = artist 
        self._track_name = track_name
        self._album = album 
        self._year = year 
        self._runtime = runtime
        
  
    def to_dict(self):
        ret = super().to_dict()
        ret['artist'] = self.artist
        ret['track_name']= self.track_name
        ret['album']= self.album
        ret['year']= self.year
        ret['runtime']=self.runtime
        return ret
    

    @staticmethod
    def from_dict(my_dict: dict[str:str]):
        file_from_dict = MusicFile(my_dict['original_path'], my_dict['file_type'])
        file_from_dict.new_path = my_dict['new_path']
        file_from_dict.size = my_dict['size']
        file_from_dict.creation_time = my_dict['creation_time']
        file_from_dict.modification_time = my_dict['modification_time']
        file_from_dict.last_access_time = my_dict['last_access_time']
        file_from_dict.artist = my_dict['artist']
        file_from_dict.track_name = my_dict['track_name']
        file_from_dict.album = my_dict['album']
        file_from_dict.year = my_dict['year']
        # file_from_dict.runtime = my_dict['runtime']
        return file_from_dict
    
    @property
    def artist(self) -> str:
        return self._artist
    
    @artist.setter
    def artist(self, a:str) ->str:
        self._artist = a

    @property
    def track_name(self) -> str:
        return self._track_name
    
    @track_name.setter
    def track_name(self, t:str) ->str:
        self._track_name = t


    @property
    def album(self) -> str:
        return self._album
    
    @album.setter
    def artist(self, al:str) ->str:
        self._album = al

    @property
    def year(self) -> str:
        return self._year
    
    @year.setter
    def year(self, y:str) ->str:
        self._year = y

        
    @property
    def runtime(self) -> str:
        return self._runtime
    
    @runtime.setter
    def runtime(self, r:str) ->str:
        self._runtime = r
'''