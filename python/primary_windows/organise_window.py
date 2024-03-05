from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QCheckBox, QDirModel, QColumnView, QHBoxLayout, QPushButton, QMessageBox, QVBoxLayout, \
    QVBoxLayout, QLabel, QTreeView, QWidget
from python.modules.organise_by_type import organise_by_type_func
from python.modules.revert_changes import revert_changes
from python.ui.drag_drop import *
from python.ui.custom_file_system_model import *
from python.model.FileSystemCache import FileSystemCache
from python.model.FileSystemNodeModel import File, Directory


class OrganiseWindow(QWidget):
    def __init__(self, window_index: int, fileSystemModel):
        super().__init__()
        self.fileSystemModel = fileSystemModel
        self.organised = []
        self.window_index = window_index
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

        # Add a checkbox for all files
        self.allCheckbox = QCheckBox('All files', self)
        right_layout.addWidget(self.allCheckbox)

        # Add a button to trigger file organization
        self.organizeButton = QPushButton("Organize Files")
        self.organizeButton.clicked.connect(self.onOrganizeClicked)
        right_layout.addWidget(self.organizeButton)

        # Add revert button to trigger revert changes after organizing
        self.revertButton = QPushButton("Revert Changes")
        self.revertButton.clicked.connect(self.onRevertClicked)
        right_layout.addWidget(self.revertButton)
        self.revertButton.setDisabled(True)

        # Ensure that the organize button stays at the bottom
        right_layout.addStretch()

        # Add the column view and the VBox to the main layout
        layout.addWidget(self.column_view)
        layout.addLayout(right_layout)

        # Set the layout for the widget
        self.setLayout(layout)

    def onOrganizeClicked(self):
        paths_to_organize = []
        allSelected = self.allCheckbox.isChecked()

        # Check if there are files dropped in drag-and-drop area
        if self.dragDropLabel.droppedFiles:
            print(f"FILES PRESENT IN DROPBOX:\n{self.dragDropLabel.droppedFiles}")
            paths_to_organize = self.dragDropLabel.droppedFiles
            paths_to_organize = [x.rstrip('/') for x in paths_to_organize]
            print(f"Paths to organise:\n{paths_to_organize}")

        # Check if there is a selection in the tree view
        elif self.column_view.currentIndex().isValid():
            tree_view_path = self.model.filePath(self.column_view.currentIndex())
            if tree_view_path:
                paths_to_organize.append(tree_view_path)
        elif allSelected:
            paths_to_organize = [self.fileSystemModel.path]

        # If there are paths to organize, either from drag-and-drop or tree view
        if paths_to_organize:
            # load cache
            cache = self.fileSystemModel.cache

            # clear the previous list of organized items
            self.organised.clear()
            message = f"Do you want to organize the following items?\n\n" + "\n".join(paths_to_organize) \
                if len(paths_to_organize) < 10 else f"Do you want to organize the following items?\n\n [Many selected]"

            reply = QMessageBox.question(self, 'Organize Confirmation', message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:

                for path in paths_to_organize:

                    # get nodes from cache
                    node = cache[path]

                    if node.isinstance(File):
                        QMessageBox.information(self, 'File Selected',
                                                'Please select a directory for optimisation.',
                                                QMessageBox.Ok)
                        return

                    organise_by_type_func(node)
                    self.organised.append(node)

                # Optionally clear the drag-and-drop list after processing
                self.dragDropLabel.droppedFiles.clear()

                # Enable the revert button
                self.revertButton.setDisabled(False)

        else:
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder from the tree view or drag and drop files.', QMessageBox.Ok)

    def onRevertClicked(self):
        """
        Revert the changes made by the organize function.
        """

        if self.organised:
            message = f"Do you want to revert the previous organisation"
            reply = QMessageBox.question(self, 'Revert Confirmation', message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                for dir_node in self.organised:
                    if isinstance(dir_node, Directory):
                        # revert changes
                        revert_changes(dir_node)
                    else:
                        print(f"{dir_node} is not a directory. Skipping...")

                # Disable the revert button after processing
                self.revertButton.setDisabled(True)

                # Clear the organized list
                self.organised.clear()

        else:
            QMessageBox.information(self, 'No files to revert',
                                    'Please organise a folder using the tree view or drag and drop files before attempting revert.',
                                    QMessageBox.Ok)

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
