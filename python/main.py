import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QMessageBox, QMenuBar, QMenu, QAction
from PyQt5.QtCore import Qt, QRect, QDir
from PyQt5.QtGui import QPainter, QPainterPath
from modules.organise_by_type import organise_by_type_func


class CircularDragDropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drag and drop files here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #aaa;
            }
        ''')
        self.setFixedSize(200, 200)  # Fixed size for circle
        self.setAcceptDrops(True)
        self.droppedFiles = []  # List to store the paths of the dropped files

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # def dropEvent(self, event):
    #     files = [u.toLocalFile() for u in event.mimeData().urls()]
    #     self.setText("\n".join(files))

    def dropEvent(self, event):
        self.droppedFiles = [u.toLocalFile() for u in event.mimeData().urls()]
        self.setText("\n".join(self.droppedFiles))
        print(self.droppedFiles)

    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        path.addEllipse(0, 0, 200, 200)
        painter.setClipPath(path)
        super().paintEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.dragDropLabel = CircularDragDropLabel()  # Initialize dragDropLabel here
        self.model = QFileSystemModel()  # Make model an instance variable
        self.tree = QTreeView()  # Make tree an instance variable
        self.create_actions()  # Create actions for the menu bar
        self.createMenuBar()  # Create a menu bar for the main window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Explorer and Drag-Drop')

        # Setup the File System Model
        self.model.setRootPath('')
        self.model.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.path.expanduser('~')))
        self.tree.setColumnWidth(0, 250)
        self.tree.setSortingEnabled(True)
        # Hide all columns except the first one ("Name")
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)

        # Create Organize button
        organize_button = QPushButton("Organize")
        organize_button.clicked.connect(self.onOrganizeClicked)

        # Create Dark Mode Toggle Button
        self.toggle_button = QPushButton("Toggle Dark Mode")
        self.toggle_button.clicked.connect(self.toggleDarkMode)

        # Set vertical layout for drag-drop area and buttons
        drag_drop_layout = QVBoxLayout()
        drag_drop_layout.addWidget(self.dragDropLabel)  # Add the previously initialized dragDropLabel
        drag_drop_layout.addWidget(organize_button)
        drag_drop_layout.addWidget(self.toggle_button)

        # Set horizontal layout
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.tree)
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

    def onOrganizeClicked(self):
        paths_to_organize = []

        # Check if there are files dropped in drag-and-drop area
        if self.dragDropLabel.droppedFiles:
            paths_to_organize.extend(self.dragDropLabel.droppedFiles)

        # Check if there is a selection in the tree view
        elif self.tree.currentIndex().isValid():
            tree_view_path = self.model.filePath(self.tree.currentIndex())
            if tree_view_path:
                paths_to_organize.append(tree_view_path)

        # If there are paths to organize, either from drag-and-drop or tree view
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
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder from the tree view \
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
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

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
        self.copyAction = QAction("Copy", self)
        self.pasteAction = QAction("Paste", self)
        self.cutAction = QAction("Cut", self)
        self.helpContentAction = QAction("Help Content", self)
        self.aboutAction = QAction("About", self)
        self.appearanceAction = QAction("Appearance", self)
        self.showFilesAction = QAction("Show Files", self)
        self.toggleDarkModeAction = QAction("Toggle Dark Mode", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

