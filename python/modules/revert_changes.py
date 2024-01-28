import os
from helper_funcs import load_json, create_list_of_file_obj, move_file, save_to_json


def revert_changes():
    try:
        _revert_changes('cache/file_data.json')
    except FileNotFoundError as e:
        print(e)
        # print("Nothing to revert")


def _revert_changes(json_file_path: str):
    """
    function to revert changes and put files back in the original location

    @params
    json_file_path: str: path to JSON file containing original structure
    """
    file_dict = load_json(json_file_path)
    # print(f"File_Dict = {file_dict}")
    # create list of file objects from dictionary
    file_list = create_list_of_file_obj(file_dict)
    # print(f"File_List: {file_list}")
    files_moved = 0
    files_checked = 0
    for file in file_list:
        original_path = file.original_path
        current_path = file.current_path
        if os.path.exists(current_path) and not os.path.exists(original_path):
            move_file(current_path, original_path)
            files_moved += 1
        files_checked += 1
        file.original_path, file.current_path = file.current_path, file.original_path

    save_to_json(file_list)
    print(f"Moved: {files_moved} files, checked: {files_checked} files")


if __name__ == "__main__":
    revert_changes()
