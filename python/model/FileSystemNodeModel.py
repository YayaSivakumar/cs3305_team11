import os
from datetime import datetime
import shutil

class FileSystemCache:
    """A simple cache for storing file and directory nodes."""
    def __init__(self):
        self.cache = {}
    
    def get(self, path):
        """Get the file or directory node from the cache if it exists and is up to date."""
        if path in self.cache and not self.is_modified(path):
            return self.cache[path]
        else:
            return None
    
    def update(self, path, node):
        """Update the cache with the given file or directory node."""
        self.cache[path] = node
        node.cache_timestamp = datetime.now()
    
    def is_modified(self, path):
        """Check if the file or directory has been modified since it was last cached."""
        cached_node = self.cache.get(path, None)
        if cached_node:
            return cached_node.modification_date() != datetime.fromtimestamp(os.path.getmtime(path))
        return True

    def remove(self, path):
        """Remove a file or directory from the cache."""
        if path in self.cache:
            del self.cache[path]

class FileSystemNode:
    """Represents a file or directory in the file system."""
    def __init__(self, path, cache):
        self.path = path
        self.cache_timestamp = None
        self.cache = cache
        self.parent = None
        self.children = []

    def find_node(self, name):
        """Recursively find a node by name."""
        if self.name() == name:
            return self
        for child in self.children:
            found = child.find_node(name)
            if found:
                return found
        return None

    def print_tree(self, level=0):
        """Print the tree structure."""
        print('  ' * level + self.name())
        for child in self.children:
            child.print_tree(level + 1)
    
    def name(self):
        """Return the name of the file or directory."""
        return os.path.basename(self.path)
    
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

class File(FileSystemNode):
    def __init__(self, path, cache):
        super().__init__(path, cache)

    def __str__(self) -> str:
        return self.name()

    def extension(self):
        """Return the file's extension."""
        _, ext = os.path.splitext(self.path)
        return ext
    
    def move(self, new_path):
        """Move the file to a new location."""
        try:
            shutil.move(self.path, new_path)
            self.path = new_path
            self.cache.update(new_path, self)
        except Exception as e:
            print(f"Error moving file: {e}")



class Document(File):
    def __init__(self, path, cache):
        super().__init__(path, cache)


class Directory(FileSystemNode):
    """Represents a directory in the file system."""
    def __init__(self, path, cache):
        super().__init__(path, cache)
        self._populate()  # Populate the directory with its children
    
    def _populate(self):
        """Populate the directory with its children."""
        try:
            for item in os.listdir(self.path):
                full_path = os.path.join(self.path, item)
                if os.path.isdir(full_path):
                    child = Directory(full_path, self.cache)
                else:
                    child = File(full_path, self.cache)
                self.add_child(child)
            self.cache.update(self.path, self)
        except FileNotFoundError:
            print(f"Directory not found: {self.path}")

    def add_child(self, child):
        """Add a child file or directory."""
        self.children.append(child)
        child.parent = self

    def list_contents(self):
        """List all files and folders in the directory."""
        return [child.name() for child in self.children]
    
    def find_file(self, file_name):
        """Recursively find a file in the directory and its subdirectories."""
        for child in self.children:
            if child.name() == file_name:
                return child
            if isinstance(child, Directory):
                found = child.find_file(file_name)
                if found:
                    return found
        return None

    def find_files_by_extension(self, extension):
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
    cache = FileSystemCache()
    root_path = '/users/conor/Downloads'  # Change to your target directory
    root_directory = Directory(root_path, cache)





