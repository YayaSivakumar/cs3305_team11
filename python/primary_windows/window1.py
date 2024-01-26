'''In window1.py, window2.py, etc.,
define the UI and functionality
for each primary window.'''
from PyQt5.QtCore import QDir
# Each primary window (e.g., window1.py, window2.py)
# should be a class that extends QWidget or a relevant widget based on your needs.
# These classes should define the UI and behavior for each primary window.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QColumnView, QPushButton

from python.ui.custom_file_system_model import CustomFileSystemModel
from python.ui.drag_drop import CircularDragDropLabel


class Window1(QWidget):
    def __init__(self):
        super().__init__()

        # Create Organize button
        organize_button = QPushButton("Organize")
        organize_button.clicked.connect(self.onOrganizeClicked)
        # drag and drop
        self.dragDropLabel = CircularDragDropLabel()  # Initialize dragDropLabel here
        drag_drop_layout = QVBoxLayout()
        drag_drop_layout.addWidget(self.dragDropLabel)  # Add the previously initialized dragDropLabel
        drag_drop_layout.addWidget(organize_button)
        # Create a layout
        layout = QVBoxLayout()
        layout.addWidget(self.column_view)
        layout.addLayout(drag_drop_layout)

        # Create a label and add it to the layout
        label = QLabel("This is Window 1")
        layout.addWidget(label)


        self.model = CustomFileSystemModel()  # Make model an instance variable
        self.model.setRootPath('')
        # self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)  # Make model an instance variable
        self.column_view = QColumnView()

        # Additional labels or widgets can be added here
        # For example: layout.addWidget(QLabel("More information..."))

        # Set the layout for the widget
        self.setLayout(layout)


        # Additional initialization, if necessary

        # Tree View
        self.model.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        self.column_view.setModel(self.model)
        self.column_view.setRootIndex(self.model.index(os.path.expanduser('~')))






        # Drag and Drop
        # Set vertical layout for drag-drop area and buttons
