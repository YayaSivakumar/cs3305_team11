import os

from PyQt5.QtWidgets import QFileSystemModel


class CustomFileSystemModel(QFileSystemModel):
    """Custom model to show only directories and files in the current directory"""

    def hasChildren(self, index):
        # Always show directories
        if self.isDir(index):
            return True

        # For files, only show them if they're not in the top-level directory
        parent_dir = self.filePath(index.parent())
        return os.path.dirname(parent_dir) != self.rootPath()
