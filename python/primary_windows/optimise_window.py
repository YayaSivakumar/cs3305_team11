from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QWidget, QTabWidget, QColumnView, QHBoxLayout, QPushButton, QSplitter, QVBoxLayout, QMessageBox

from python.ui.drag_drop import *
from python.ui.custom_file_system_model import *

from python.model.FileSystemNodeModel import *
from python.modules.compress import compress
from python.modules.deduplicate import deduplicate


class OptimiseWindow(QWidget):

    def __init__(self, window_index: int, fileSystemModel):
        super().__init__()
        self.fileSystemModel = fileSystemModel
        self.organised = []
        self.window_index = window_index
        self.duplicate_files = []

        # Create main layout
        layout = QHBoxLayout(self)

        # Create the dragDropLabel
        self.dragDropLabel = CircularDragDropLabel()

        # Create a description label
        description_label = QLabel(
            "Description: Drag and drop files to the area below or select files from the column view to organize them "
            "into folders based on their file types.")
        description_label.setWordWrap(True)  # Allow text to wrap to the next line
        description_label.setAlignment(Qt.AlignTop)  # Align the text to the top

        # Initialize the model for the ColumnView
        self.model = CustomFileSystemModel()
        self.model.setRootPath(self.fileSystemModel.path)
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        # Set up the ColumnView
        self.column_view = QColumnView()
        self.column_view.setModel(self.model)
        # only show paths in cache
        self.column_view.setRootIndex(self.model.index(self.fileSystemModel.path))

        # Create a QVBoxLayout for the description label, organize button, and dragDropLabel
        right_layout = QVBoxLayout()
        right_layout.addWidget(description_label)  # Add the description label to the layout
        right_layout.addWidget(self.dragDropLabel)

        # Create a description label
        description_label = QLabel(
            "Description: Drag and drop files to the area below or select files from the column view to scan for "
            "duplicate files and compress large files. Click the 'Optimise Files' button to start the process.")
        description_label.setWordWrap(True)  # Allow text to wrap to the next line
        description_label.setAlignment(Qt.AlignTop)  # Align the text to the top

        self.duplicate_files_label = QLabel(f"{self.duplicate_files}")
        self.duplicate_files_label.setWordWrap(True)

        # Add a button to trigger file organization
        self.optimiseButton = QPushButton("Optimise Files")
        self.optimiseButton.clicked.connect(self.onOptimiseClicked)

        # Add a button to trigger duplicate file deletion
        self.deleteDuplicatesButton = QPushButton("Delete Duplicate Files")
        self.deleteDuplicatesButton.clicked.connect(self.deleteDuplicates)
        self.deleteDuplicatesButton.setDisabled(True)

        # Create a QVBoxLayout for the description label, organize button, and dragDropLabel
        right_layout = QVBoxLayout()
        right_layout.addWidget(description_label)  # Add the description label to the layout
        right_layout.addWidget(self.dragDropLabel)
        right_layout.addWidget(self.duplicate_files_label)
        right_layout.addWidget(self.optimiseButton)
        right_layout.addWidget(self.deleteDuplicatesButton)

        # Ensure that the optimise button stays at the bottom
        right_layout.addStretch()

        # Add the column view and the VBox to the main layout
        layout.addWidget(self.column_view)
        layout.addLayout(right_layout)

        # Set the layout for the widget
        self.setLayout(layout)

    def onOptimiseClicked(self):
        paths_to_optimise = []

        # Check if there are files dropped in drag-and-drop area
        if self.dragDropLabel.droppedFiles:
            print(f"FILES PRESENT IN DROPBOX:\n{self.dragDropLabel.droppedFiles}")
            paths_to_optimise = self.dragDropLabel.droppedFiles
            paths_to_optimise = [x.rstrip('/') for x in paths_to_optimise]
            print(f"Paths to organise:\n{paths_to_optimise}")

        # Check if there is a selection in the tree view
        elif self.column_view.currentIndex().isValid():
            tree_view_path = self.model.filePath(self.column_view.currentIndex())
            if tree_view_path:
                paths_to_optimise.append(tree_view_path)

        # If there are paths to organize, either from drag-and-drop or tree view
        if paths_to_optimise:

            # load cache
            cache = self.fileSystemModel.cache

            message = f"Do you want to organize the following items?\n\n" + "\n".join(paths_to_optimise)
            reply = QMessageBox.question(self, 'Optimise Confirmation', message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:

                for path in paths_to_optimise:
                    # get nodes from cache
                    node = cache[path]

                    if node.isinstance(File):
                        QMessageBox.information(self, 'File Selected',
                                                'Please select a directory for optimisation.',
                                                QMessageBox.Ok)
                        return

                    # check for duplicate files in directory
                    self.duplicate_files = deduplicate(node)

                    # compress large files
                    self.checkCompressFiles(node)

                    if self.duplicate_files:
                        QMessageBox.information(self, 'Success',
                                                f'Duplicates found in {path}.',
                                                QMessageBox.Ok)
                        # update label
                        duplicate_paths = [file.path for file in self.duplicate_files]
                        reformatted_duplicates = "\n".join(duplicate_paths)
                        self.duplicate_files_label.setText(f"{reformatted_duplicates}")
                        self.deleteDuplicatesButton.setDisabled(False)
                    else:
                        QMessageBox.information(self, 'Success',
                                                f'No duplicates found in {path}.',
                                                QMessageBox.Ok)
            else:
                QMessageBox.information(self, 'No Selection',
                                        'Please select a file or folder from the tree view or drag and drop files.',
                                        QMessageBox.Ok)

    def deleteDuplicates(self):
        # delete functionality will be implemented here once scan functionality is implemented for FileSystemNodeModel

        for file in self.duplicate_files:
            # delete file
            file.delete()

        self.duplicate_files.clear()
        self.duplicate_files_label.setText('[]')
        self.deleteDuplicatesButton.setDisabled(True)

    def checkCompressFiles(self, dir_node):
        for node in dir_node.children[:]:
            if node.size > 4000000000:
                # compress file
                compress(node)
                # delete original file
                node.delete()

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
