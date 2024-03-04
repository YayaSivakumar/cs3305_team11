from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from python.model.FileSystemCache import FileSystemCache
from python.model.FileSystemNodeModel import *
import os


class SplashWindow(QWidget):
    fileSystemModelReady = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.scanThread = None
        self.folderSelection = None
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Heading
        heading = QLabel("Welcome to the FileSystem Scanner")
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)

        # Dropdown (Combo Box) for folder selection
        self.folderSelection = QComboBox(self)
        user_paths = {
            "Downloads": os.path.expanduser('~')+'/Downloads',
            "Desktop": os.path.expanduser('~')+'/Desktop',
            "Documents": os.path.expanduser('~')+'/Documents',
        }
        print(user_paths)
        for name, path in user_paths.items():
            self.folderSelection.addItem(name, path)
        layout.addWidget(self.folderSelection)

        # Scan button
        scan_btn = QPushButton("Scan")
        scan_btn.clicked.connect(self.on_scan_clicked)
        layout.addWidget(scan_btn)

        self.setLayout(layout)
        self.setWindowTitle("K.L.A.A.S. - Knowledge Lookup and Access System")

    def on_scan_clicked(self):
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
        if fileSystemModel:
            self.fileSystemModelReady.emit(fileSystemModel)
        self.close()


class ScanThread(QThread):
    scanComplete = pyqtSignal(object)

    def __init__(self, path, cache):
        super().__init__()
        self.path = path
        self.cache = cache

    def run(self):
        if os.path.isdir(self.path):
            fileSystemModel = Directory(self.path, self.cache)
            self.scanComplete.emit(fileSystemModel)  # Emit the model after scanning
        else:
            self.scanComplete.emit(None)  # Emit None or handle error appropriately
