import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QAction, QColumnView
from PyQt5.QtCore import QDir
from modules.organise_by_type import organise_by_type_func
from python.ui.custom_file_system_model import CustomFileSystemModel
from python.ui.drag_drop import CircularDragDropLabel

# Main Application (main.py):
# This script initializes and displays the main window.
# It's responsible for setting up the QApplication and starting the event loop.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.dragDropLabel = CircularDragDropLabel()  # Initialize dragDropLabel here
        self.model = CustomFileSystemModel()  # Make model an instance variable
        self.model.setRootPath('')
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)  # Make model an instance variable
        self.column_view = QColumnView()
        self.create_actions()  # Create actions for the menu bar
        self.createMenuBar()  # Create a menu bar for the main window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Explorer and Drag-Drop')
        # Setup the File System Model
        self.model.setRootPath('')
        self.model.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        self.column_view.setModel(self.model)
        self.column_view.setRootIndex(self.model.index(os.path.expanduser('~')))



        # Create Organize button
        organize_button = QPushButton("Organize")
        organize_button.clicked.connect(self.onOrganizeClicked)

        # Set vertical layout for drag-drop area and buttons
        drag_drop_layout = QVBoxLayout()
        drag_drop_layout.addWidget(self.dragDropLabel)  # Add the previously initialized dragDropLabel
        drag_drop_layout.addWidget(organize_button)

        # Set horizontal layout
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.column_view)
        h_layout.addLayout(drag_drop_layout)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(h_layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(300, 300, 1000, 600)

    def toggleDarkMode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            # Dark mode styles
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #2e2e2e;
                }
                QLabel {
                    color: #fff;
                }
                QTreeView {
                    background-color: #393939;
                    color: #fff;
                }
                QPushButton {
                    background-color: #5e5e5e;
                    color: #fff;
                    border: 1px solid #2e2e2e;
                }
                QMessageBox {
                    background-color: #393939;
                    color: #fff;
                }
            ''')
        else:
            # Light mode styles (default)
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QLabel {
                    color: #000;
                }
                QTreeView {
                    background-color: #fff;
                    color: #000;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000;
                    border: 1px solid #d3d3d3;
                }
            ''')

        self.toggleDarkModeAction.setText("Toggle Light Mode" if self.dark_mode else "Toggle Dark Mode")
    def onOrganizeClicked(self):
        paths_to_organize = []

        # Check if there are files dropped in drag-and-drop area
        if self.dragDropLabel.droppedFiles:
            paths_to_organize.extend(self.dragDropLabel.droppedFiles)

        # Check if there is a selection in the column_view
        elif self.column_view.currentIndex().isValid():
            column_view_path = self.model.filePath(self.column_view.currentIndex())
            if column_view_path:
                paths_to_organize.append(column_view_path)

        # If there are paths to organize, either from drag-and-drop or column_view
        if paths_to_organize:
            message = f"Do you want to organize the following items?\n\n" + "\n".join(paths_to_organize)
            reply = QMessageBox.question(self, 'Organize Confirmation', message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                for path in paths_to_organize:
                    print(f"Organizing: {path}")
                    # Call Bash script with each path
                    organise_by_type_func(path)

                # Optionally clear the drag-and-drop list after processing
                self.dragDropLabel.droppedFiles.clear()

        else:
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder from the column_view \
            or drag and drop files.', QMessageBox.Ok)

    def createMenuBar(self):
        menuBar = self.menuBar()

        # File menu
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)

        viewMenu = menuBar.addMenu("View")
        viewMenu.addAction(self.showFilesAction)
        appearanceMenu = viewMenu.addMenu("Appearance")
        appearanceMenu.addAction(self.toggleDarkModeAction)

    def create_actions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("New")
        # Creating actions using the second constructor
        self.openAction = QAction("Open...", self)
        self.saveAction = QAction("Save", self)
        self.exitAction = QAction("Exit", self)

        self.undoAction = QAction("Undo", self)
        self.undoAction.triggered.connect(self.undo_action)


        self.redoAction = QAction("Redo", self)
        self.redoAction.triggered.connect(self.redo_action)

        self.helpContentAction = QAction("Help Content", self)
        self.aboutAction = QAction("About", self)

        self.appearanceAction = QAction("Appearance", self)
        self.showFilesAction = QAction("Show Files", self)
        self.toggleDarkModeAction = QAction("Toggle Dark Mode", self)
        self.toggleDarkModeAction.triggered.connect(self.toggleDarkMode)

    def undo_action(self):
        self.undoAction.setEnabled(False)
#       Call to backend function

    def redo_action(self):
        self.redoAction.setEnabled(False)
#       Call to backend function

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

