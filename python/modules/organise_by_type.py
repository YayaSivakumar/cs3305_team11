# script name: sort.py
import os
import shutil

def determine_filetype(filename: str) -> str:
    extension = filename.split('.')
    print(f"ext: {extension}")
    types = {'documents':['pdf', 'docx', 'doc', 'txt', 'text'], \
             'photos':['jpeg', 'jpg', 'svg', 'png', 'PNG'],\
             'videos': ['mp4', 'mov', 'avi'],\
             'music': ['wav', 'mp3', 'aac']}
    
    for category in types:
        if extension in types[category]:
            return category
        

    return 'misc'

def create_target_directories(filepath: str):
    os.makedirs(filepath+'/Documents')
    os.makedirs(filepath+'/Photos')
    os.makedirs(filepath+'/Videos')
    os.makedirs(filepath+'/Music')
    os.makedirs(filepath+'/Misc')

def get_pwd():
    return os.getcwd()

def list_dir(filepath: str):
    print(os.listdir(filepath))

if __name__ == "__main__":
    create_target_directories('/Users/jackmoloney/Desktop/test')
    list_dir('/Users/jackmoloney/Desktop/test')