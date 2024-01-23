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