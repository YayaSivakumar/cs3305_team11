import os
import zipfile


def compress_dir(file_list, dir_name):
    # create a ZipFile object
    archive_path = os.path.dirname(file_list[0]) + '/' + dir_name + '.zip'

    with zipfile.ZipFile(archive_path, 'w') as zipf:
        for file in file_list:
            if file != archive_path:
                zipf.write(file, os.path.basename(file))

    return archive_path


if __name__ == '__main__':
    # usage
    '''
    file_list = ['/Users/yachitrasivakumar/Desktop/files/Screenshot 2024-02-28 at 17.58.46.png', '/Users/yachitrasivakumar/Desktop/files/Screenshot 2024-02-28 at 18.36.46.png', '/Users/yachitrasivakumar/Desktop/files/Screenshot 2024-03-04 at 16.24.45.png']
    dir_name = 'archive_folder'
    print(compress_dir(file_list, dir_name))'''
