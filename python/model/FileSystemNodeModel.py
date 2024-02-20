from __future__ import annotations
import os
from datetime import datetime
import shutil
import hashlib


class FileSystemNode:
    """Represents a file or directory in the file system."""

    def __init__(self, path: str, cache: FileSystemCache):
        self.path = path
        self.name = None
        self.revert_path = path
        self.cache_timestamp = None
        self.cache = cache
        self.parent = None
        self.children = []

    def find_node(self, name: str):
        """Recursively find a node by name."""
        if self.name() == name:
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
        print('  ' * level + self.name())
        for child in self.children:
            child.print_tree(level + 1)

    def name(self):
        """Return the name of the file or directory."""
        return self.name

    def size(self):
        """Return the size of the file in bytes."""
        try:
            return os.path.getsize(self.path)
        except FileNotFoundError:
            return 0

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
        return self.name().startswith('.')

    def move(self, new_path: str):
        """Move the node to a new location."""
        try:
            shutil.move(self.path, new_path)
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
        except Exception as e:
            print(f"Error moving Obj: {e}")

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


class File(FileSystemNode):
    def __init__(self, path: str, cache: FileSystemCache):
        super().__init__(path, cache)
        self.name = os.path.basename(path)  # give file a name

    def __str__(self) -> str:
        return self.name

    def extension(self):
        """Return the file's extension."""
        _, ext = os.path.splitext(self.path)
        return ext


class Directory(FileSystemNode):
    """Represents a directory in the file system."""

    def __init__(self, path: str, cacheObj: FileSystemCache):
        super().__init__(path, cacheObj)
        self.name = os.path.basename(path.rstrip(os.sep))
        self._populate()  # Populate the directory with its children
        cacheObj.save_to_file()

    def _populate(self):
        """Populate the directory with its children."""
        try:
            for item in os.listdir(self.path):
                full_path = os.path.join(self.path, item)
                if os.path.isdir(full_path):
                    child = Directory(full_path, self.cache)
                    self.cache.update(child.path, child)
                else:
                    child = File(full_path, self.cache)
                    self.cache.update(child.path, child)
                self.add_child(child)
            self.cache.update(self.path, self)
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
        return [child.name() for child in self.children]

    def find_file(self, file_name: str):
        """Recursively find a file in the directory and its subdirectories."""
        for child in self.children:
            if child.name() == file_name:
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
                print(f"Found file: {child.name()}")  # Print the file path
            elif isinstance(child, Directory):
                matching_files.extend(child.find_files_by_extension(extension))

        return matching_files


if __name__ == '__main__':
    '''
    from dotenv import load_dotenv

    cache = FileSystemCache()

    load_dotenv()

    env_path: str = os.getenv('ROOT_PATH')
    if env_path:
        print('Running on path as given in .env file')
        root_directory = Directory(env_path, cache)
        cache.save_to_file()
    else:
        print("DOCUMENTS_PATH environment variable is not set.")
        root_path = '/add/a/path/here'  # Change to your target directory
        root_directory = Directory(root_path, cache)
    root_directory.print_tree()

    print("Attempting to load cache from pkl")
    cache = FileSystemCache()
    print("Before load:")
    print(cache)
    cache.load_from_file()
    print("After load:")
    print(cache)

    print("Testing find node by name")
    search = root_directory.find_node_from_cache('/Users/jackmoloney/Downloads/Jordan B. Peterson - 12 Rules for '
                                                 'Life_ An Antidote to Chaos-Random House Canada (2018).epub')
    print(search, type(search))
'''