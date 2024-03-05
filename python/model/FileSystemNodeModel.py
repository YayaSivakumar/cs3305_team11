from __future__ import annotations
import os
from datetime import datetime
import shutil
import hashlib

from PyQt5.QtCore import QRunnable, QThreadPool


class FileSystemNode:
    """Represents a file or directory in the file system."""

    def __init__(self, path: str, cache: FileSystemCache, parent):
        self.path = path
        self.name = None
        self.revert_path = path
        self.cache_timestamp = None
        self.cache = cache
        self.parent = parent if parent else None
        self.children = []
        self.size = None

    def find_node(self, name: str):
        """Recursively find a node by name."""
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_node(name)
            if found:
                return found
        return None

    def find_node_from_cache(self, name: str) -> FileSystemNode:
        try:
            return self.cache[name]
        except KeyError:
            raise Exception(f"File {name} not found.")

    def print_tree(self, level=0):
        """Print the tree structure.
            Level is used for recursive call, param not to be used for testing per say
        """
        print('  ' * level + self.name)
        for child in self.children:
            child.print_tree(level + 1)

    def name(self):
        """Return the name of the file or directory."""
        return self.name

    def get_size(self):
        """Return the size of the file in bytes."""
        if self.size is None:
            try:
                self.size = os.path.getsize(self.path)
            except FileNotFoundError:
                self.size = 0
        return self.size
        # try:
        #     return os.path.getsize(self.path)
        # except FileNotFoundError:
        #     return 0

    def creation_date(self):
        """Return the creation date of the file."""
        return datetime.fromtimestamp(os.path.getctime(self.path))

    def modification_date(self):
        """Return the modification date of the file."""
        return datetime.fromtimestamp(os.path.getmtime(self.path))

    def delete(self):
        """Delete the file or directory."""
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)
        if self.parent:
            self.parent.children.remove(self)
        self.cache.remove(self.path)

    def change_permissions(self, mode):
        """Change the permissions of the file."""
        os.chmod(self.path, mode)

    def is_invisible(self):
        """Check if the file is hidden."""
        return self.name.startswith('.')

    # def move(self, new_path: str):
    #     """Move the node to a new location."""
    #     try:
    #         shutil.move(self.path, new_path)
    #         # update paths
    #         self.revert_path = self.path
    #         self.path = new_path
    #         # update data structure
    #         self.parent.remove_child(self)
    #         self.parent = self.cache[os.path.dirname(new_path)]
    #         self.parent.add_child(self)
    #         # update cache
    #         self.cache.remove(self.revert_path)
    #         self.cache.update(new_path, self)
    #     except Exception as e:
    #         print(f"Error moving Obj: {e}")

    def move(self, dst: str):
        try:
            # Try using shutil.move first
            shutil.move(self.path, dst)
            self._move_update_metadata(dst)
        except Exception as e:
            print(f"shutil.move failed: {e}")
            # If shutil.move fails, manually copy and then delete
            try:
                shutil.copy2(self.path, dst)  # copy2 preserves metadata
                os.remove(self.path)
                self._move_update_metadata(dst)
            except Exception as e:
                print(f"Manual copy and delete failed: {e}")

    def _move_update_metadata(self, new_path):
        # update paths
        self.revert_path = self.path
        self.path = new_path
        # update data structure
        self.parent.remove_child(self)
        self.parent = self.cache[os.path.dirname(new_path)]
        self.parent.add_child(self)
        # update cache
        self.cache.remove(self.revert_path)
        self.cache.update(new_path, self)

    def to_json(self):
        return {
            'path': self.path,
            'revert_path': self.revert_path,
            'cache_timestamp': self.cache_timestamp,
            'cache': self.cache,
            'parent': self.parent,
            'self.children': self.children
        }

    def get_hashed_value(self):
        """
        Hashes the contents of a file using SHA-256 and returns the hash in hexadecimal format.

        Parameters:
        - filepath: Path to the file to be hashed.

        Returns:
        - A hexadecimal string representation of the hash of the file's contents.
        """
        sha256_hash = hashlib.sha256()

        try:
            if os.path.isdir(self.path):
                return None
            else:
                # open file
                with open(self.path, "rb") as f:
                    # read contents in chunks to avoid memory issues
                    for byte_block in iter(lambda: f.read(4096), b""):
                        # update hashed value with each chunk
                        sha256_hash.update(byte_block)
                # return in hexadecimal format
                return sha256_hash.hexdigest()
        except FileNotFoundError:
            print(f"File not found: {self.path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def search(self, search_term: str):
        """Search for nodes including search_term in cache"""
        if search_term in self.cache.keyword_index:
            print("Keyword found")
            result_list = list(self.cache.keyword_index[search_term])
            return result_list
        # no matches found
        print("Keyword not found")
        return []

    def isinstance(self, obj_type: object):
        """Check if the node is an instance of the given type."""
        return isinstance(self.__class__, obj_type)


class File(FileSystemNode):
    def __init__(self, path: str, cache: FileSystemCache, name, parent):
        super().__init__(path, cache, parent)
        self.name = name  # give file a name

    def __str__(self) -> str:
        return self.name

    def extension(self):
        """Return the file's extension."""
        _, ext = os.path.splitext(self.path)
        return ext


class Directory(FileSystemNode):
    """Represents a directory in the file system."""

    def __init__(self, path: str, cacheObj: FileSystemCache, name, parent):
        super().__init__(path, cacheObj, parent=parent)
        self.name = name
        self._populate()  # Populate the directory with its children
        cacheObj.save_to_file()

    def _populate(self):
        """Populate the directory with its children."""
        try:
            with os.scandir(self.path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        if '.' in entry.path:
                            continue
                        child = Directory(entry.path, self.cache, name=entry.name, parent=self)
                    else:
                        child = File(entry.path, self.cache, name=entry.name, parent=self)
                        self.cache.update(child.path, child)
                    self.add_child(child)
            self.cache.update(self.path, self)
        except FileNotFoundError:
            print(f"Directory not found: {self.path}")

    def _multithread_populate(self):
        thread_pool = QThreadPool.globalInstance()

        # define callback function to add children from threads
        def add_child(child):
            self.children.append(child)

        try:
            with os.scandir(self.path) as entries:
                for entry in entries:
                    task = ScanTask(entry, self.cache, add_child)
                    thread_pool.start(task)
        except FileNotFoundError:
            print(f"Directory not found: {self.path}")

    def add_child(self, child: object):
        """Add a child file or directory."""
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: object):
        """Remove a child file or directory."""
        self.children.remove(child)

    def list_contents(self):
        """List all files and folders in the directory."""
        return [child.name for child in self.children]

    def find_file(self, file_name: str):
        """Recursively find a file in the directory and its subdirectories."""
        for child in self.children:
            if child.name == file_name:
                return child
            if isinstance(child, Directory):
                found = child.find_file(file_name)
                if found:
                    return found
        return None

    def find_files_by_extension(self, extension: str):
        """Recursively find all files with a given extension in the directory and its subdirectories."""
        matching_files = []  # List of matching files
        for child in self.children:  # Iterate over the children
            if isinstance(child, File) and child.extension() == extension:
                matching_files.append(child)
                print(f"Found file: {child.name}")  # Print the file path
            elif isinstance(child, Directory):
                matching_files.extend(child.find_files_by_extension(extension))

        return matching_files

    def calculate_folder_size(self) -> list[FileSystemNode]:
        for child in self.children:
            child.get_size()
        return self.children



class ScanTask(QRunnable):
    def __init__(self, entry:os.DirEntry, cache, add_child_callback):
        super().__init__()
        self.entry = entry
        self.cache = cache
        self.add_child_callback = add_child_callback

    def run(self):
        if self.entry.is_dir():
            child = Directory(self.entry.path, self.cache)
        else:
            child = File(self.entry.path, self.cache)

        self.cache.update(child.path, child)
        self.add_child_callback(child)


if __name__ == '__main__':
    pass