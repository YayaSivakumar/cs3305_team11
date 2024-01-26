'''In mainwindow.py, create the main window with a sidebar.
In the sidebar's slot method, change the displayed widget
in the QStackedWidget based on the user's choice.'''

import os
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox, QAction, QColumnView, \
    QMainWindow, QListWidget, QListWidgetItem
from modules.organise_by_type import organise_by_type_func
from python.ui.custom_file_system_model import CustomFileSystemModel
from python.ui.drag_drop import CircularDragDropLabel


# This is the central window that includes the sidebar and the area where primary windows will be displayed.
# Use a QStackedWidget or QStackedLayout to manage the primary windows.
# This allows you to stack the different windows on top of each other and switch between them.
# The sidebar can be implemented using QListWidget or QToolBar,
# with each item or button connected to a slot that changes the displayed widget in the QStackedWidget.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.h_layout = QHBoxLayout()
        self.dark_mode = False

        self.setWindowTitle('File Explorer and Drag-Drop')
        # Setup the File System Model

        # Set the geometry of the main window
        self.setGeometry(300, 300, 1000, 600)

        # sidebar
        self.sidebar = QListWidget()
        sidebar_organisation = QListWidgetItem("Organise")
        self.sidebar.addItem(sidebar_organisation)
        sidebar_music = QListWidgetItem("Music")
        self.sidebar.addItem(sidebar_music)
        # learn how to make sidebar have min x and min y, and remain static in size
        self.sidebar.setGeometry(300, 300, 200, 600)
        self.h_layout.addWidget(self.sidebar)

        # Primary window
        self.primary_window = QWidget()
        self.primary_window_layout = QVBoxLayout() # decide on primary windows layout?
        #  think the primary window should not need a layout or have layout but only will ever have one item which is
        #  the window that we call in
        self.h_layout.addWidget(self.primary_window)

        # Central Widget (Main Window Frame)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.h_layout)
        self.setCentralWidget(self.central_widget)

        # Menu Bar & Actions
        self.create_actions()  # Create actions for the menu bar
        self.createMenuBar()  # Create a menu bar for the main window



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