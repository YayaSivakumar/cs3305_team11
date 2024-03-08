from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QComboBox, QSplitter, QSizePolicy, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from python.model.FileSystemCache import FileSystemCache
from python.model.FileSystemNodeModel import *
import os

class SplashWindow(QWidget):
    """
    Splash window for the application. This is the first window that the user sees.
    It allows the user to select a folder to scan and then proceeds to the main window.
    """
    fileSystemModelReady = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.scanThread = None
        self.folderSelection = None
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        # Main layout of the entire window
        main_layout = QVBoxLayout(self)

        # Top widget occupies 70% of the space
        top_widget = QWidget(self)
        top_widget_layout = QVBoxLayout(top_widget)
        main_layout.addWidget(top_widget)
        main_layout.setStretchFactor(top_widget, 7)

        # Bottom widget occupies the remaining 30% of the space
        bottom_widget = QWidget(self)
        bottom_layout = QVBoxLayout(bottom_widget)
        main_layout.addWidget(bottom_widget)
        main_layout.setStretchFactor(bottom_widget, 3)

        # Top left widget (60% of the top layout)
        top_left_widget = QWidget(top_widget)
        top_left_layout = QVBoxLayout(top_left_widget)
        heading = QLabel("Welcome to the FileSystem Scanner")
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("font-size: 30px; font-weight: bold")
        top_left_layout.addWidget(heading)
        top_widget_layout.addWidget(top_left_widget)
        top_widget_layout.setStretchFactor(top_left_widget, 6)

        # Top right widget (40% of the top layout)
        top_right_widget = QLabel(top_widget)
        top_right_widget.setAlignment(Qt.AlignCenter)  # Center the image in the label
        pixmap = QPixmap('python/ui/images/icons/top_right_background.png')  # Replace with the correct path
        top_right_widget.setPixmap(pixmap)
        top_right_widget.setScaledContents(True)
        top_widget_layout.addWidget(top_right_widget)
        top_widget_layout.setStretchFactor(top_right_widget, 4)

        # Add a label to above the combo box
        label = QLabel("Select a folder to scan")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold")
        bottom_layout.addWidget(label)

        # Dropdown (Combo Box) for folder selection
        self.folderSelection = QComboBox()
        self.folderSelection.setStyleSheet("""
                    QComboBox {
                        font-size: 16px; /* Larger font size */
                        padding: 2px 10px; /* Add some padding */
                    }
                """)

        # Size policy for ComboBox to not stretch
        self.folderSelection.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        user_paths = {
            "Downloads": os.path.expanduser('~') + '/Downloads/',
            "Desktop": os.path.expanduser('~') + '/Desktop/',
            "Documents": os.path.expanduser('~') + '/Documents/',
            "Home Folder": os.path.expanduser('~')
        }
        for name, path in user_paths.items():
            self.folderSelection.addItem(name, path)
        bottom_layout.addWidget(self.folderSelection)

        # Wrapper for combo box to manage width and alignment
        combo_wrapper_widget = QWidget()
        combo_wrapper_layout = QHBoxLayout(combo_wrapper_widget)
        combo_wrapper_layout.addStretch()
        combo_wrapper_layout.addWidget(self.folderSelection)
        combo_wrapper_layout.addStretch()

        bottom_layout.addWidget(combo_wrapper_widget)

        # Scan button
        scan_btn = QPushButton("Scan")
        scan_btn.clicked.connect(self.on_scan_clicked)

        # Button styling
        scan_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    color: #ffffff;
                    background-color: #5c6bc0;
                    border-radius: 10px;
                    padding: 10px;
                    min-width: 100px;
                    max-width: 200px;
                }
                QPushButton:hover {
                    background-color: #3949ab;
                }
                QPushButton:pressed {
                    background-color: #283593;
                }
            """)

        # Button size policy
        scan_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Add the button to the layout with a wrapper widget for proper alignment
        btn_wrapper_widget = QWidget()
        btn_wrapper_layout = QHBoxLayout(btn_wrapper_widget)
        btn_wrapper_layout.addStretch()
        btn_wrapper_layout.addWidget(scan_btn)
        btn_wrapper_layout.addStretch()
        bottom_layout.addWidget(btn_wrapper_widget)

        # Set the main layout to the window
        self.setLayout(main_layout)
        self.setWindowTitle("K.L.A.A.S. - Knowledge Lookup and Access System")

    def on_scan_clicked(self):
        """
        This method is called when the user clicks the scan button.
        """
        selected_path = self.folderSelection.currentData()  # Get the selected path
        FSCache = FileSystemCache()
        # attempt to load from cache
        if not FSCache.load_from_file() or selected_path not in FSCache.body:
            print('no cache found, scanning')

            self.scanThread = ScanThread(selected_path, FSCache)
            self.scanThread.scanComplete.connect(self.handle_scan_complete)
            self.scanThread.start()
        else:
            fileSystemModel = FSCache[selected_path]
            self.fileSystemModelReady.emit(fileSystemModel)
            self.close()

    def handle_scan_complete(self, fileSystemModel):
        """
        This method is called when the scan thread completes.
        """
        if fileSystemModel:
            self.fileSystemModelReady.emit(fileSystemModel)
        self.close()


class ScanThread(QThread):
    """
    This class is a QThread that scans the file system in the background.
    """
    scanComplete = pyqtSignal(object)

    def __init__(self, path, cache):
        super().__init__()
        self.path = path
        self.cache = cache

    def run(self):
        if os.path.isdir(self.path):
            fileSystemModel = Directory(self.path, self.cache, name=os.path.dirname(self.path), parent=None)
            self.scanComplete.emit(fileSystemModel)  # Emit the model after scanning
        else:
            self.scanComplete.emit(None)  # Emit None or handle error appropriately
