import os
import shutil
import datetime

def main(path_to_organise):
    md_dict = get_metadata_from_files(get_file_paths(path_to_organise))
    organise_by_date(md_dict, path_to_organise)

def size_convert(size: int) -> str:
    """
    function to convert bytes to kilobytes

    @params
    size: int: size in bytes
    ret: str: size in kilobytes
    """
    return str(round(size/1000, 2)) + ' KB'

def time_convert(timestamp: int) -> str:
    """
    function to convert time to a readable format

    @params
    time: int: time in seconds
    ret: str: time in readable format
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_file_paths(path):
    """
    function to get the paths of all files in a directory
    
    @params
    path: str: path to root directory
    """
    files_list = []
    # walk through all of the files in the specified path
    for root, dirs, files in os.walk(path):
        for file in files:
            # ignore directories and append file path to the list
            files_list.append(os.path.join(root, file))
    return files_list

def get_metadata_from_files(filepath_list: list):
    """
    function to get the metadata from a file 

    @params
    filepath: str: absolute path to a file
    """

    accepted_filetypes = ['pdf', 'docx', 'doc', 'txt', 'text', 'jpeg', 'jpg', 'svg', 'png', 'PNG', 'mp4', 'mov', 'avi', 'wav', 'mp3', 'aac', 'webp']
    md_dict = {}

    # get the time data from each file
    for filepath in filepath_list:

        stats = os.stat(filepath)
        
        attrs = {
            'Absolute Path': filepath,
            'File Type': filepath.split('.')[-1],
            'Size (KB)': size_convert(stats.st_size),
            'Creation Time': time_convert(stats.st_ctime),
            'Modified Time': time_convert(stats.st_mtime),
            'Last Access Time': time_convert(stats.st_atime),
        }

        # do not include invisible files
        if attrs['File Type'] in accepted_filetypes:
            md_dict[filepath] = attrs 
        else:
            print(filepath, 'is not an accepted filetype')

    return md_dict

def move_file(source: str, dest: str):
    try:
        shutil.move(source, dest)
    except IOError as e:
        print(f"Error: {e}")

def organise_by_date(md_dict: dict, directory_path: str):
    """
    function to create the required directories

    @params
    filepath: str: path to create directories at
    required: list[str]: list of the required folders
    """
    month_names = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June',\
                   '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
    
    # iterate through each file and obtain year and month of modification(/creation/last access)
    for key, values in md_dict.items():
        # get list of directories already created in path
        list_of_directories = os.listdir(directory_path)
        # get year and month of modification
        year = values['Modified Time'].split('-')[0] # the reason for using 'Modified Time' in this function is because the 'Creation Time' values changed when I moved them into test_by_date folder
        month = month_names[values['Modified Time'].split('-')[1]] # for test purposes I am using the 'Modified Time' values

        # create directories if they don't already exist
        if year not in list_of_directories:
            os.makedirs(directory_path+'/'+year)
        if month not in os.listdir(directory_path+'/'+year):
            os.makedirs(directory_path+'/'+year+'/'+month)

        # move file to the correct directory
        move_file(key, directory_path+'/'+year+'/'+month)

if __name__ == "__main__":
    main(os.getcwd()+"/test_by_date")