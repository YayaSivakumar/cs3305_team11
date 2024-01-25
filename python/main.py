import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QMessageBox
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
        organizeButton = QPushButton("Organize")
        organizeButton.clicked.connect(self.onOrganizeClicked)

        # Create Dark Mode Toggle Button
        self.toggleButton = QPushButton("Toggle Dark Mode")
        self.toggleButton.clicked.connect(self.toggleDarkMode)

        # Set vertical layout for drag-drop area and buttons
        dragDropLayout = QVBoxLayout()
        dragDropLayout.addWidget(self.dragDropLabel)  # Add the previously initialized dragDropLabel
        dragDropLayout.addWidget(organizeButton)
        dragDropLayout.addWidget(self.toggleButton)

        # Set horizontal layout
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.tree)
        hLayout.addLayout(dragDropLayout)

        # Central Widget
        centralWidget = QWidget()
        centralWidget.setLayout(hLayout)
        self.setCentralWidget(centralWidget)
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
                    # call python function to organise by type
                    organise_by_type_func(path)

                # Optionally clear the drag-and-drop list after processing
                self.dragDropLabel.droppedFiles.clear()

        else:
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder from the tree view \
            or drag and drop files.', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
