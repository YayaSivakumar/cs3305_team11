import os
import threading
from dotenv import load_dotenv
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QStackedLayout, QPushButton
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from python.model.FileSystemNodeModel import *
from python.model.FileSystemCache import FileSystemCache

load_dotenv()


# Custom widget that includes a label for the filename and a label for the file path
class FileListItem(QWidget):
    def __init__(self, filename, filepath, parent=None):
        super(FileListItem, self).__init__(parent)
        self.layout = QVBoxLayout(self)  # Use QVBoxLayout for vertical stacking

        self.filenameLabel = QLabel(filename)
        self.filenameLabel.setStyleSheet("font-size: 16px;")  # Larger font size for filenames
        self.filepathLabel = QLabel(filepath)
        self.filepathLabel.setStyleSheet(
            "color: grey; font-size: 12px;")  # Smaller font size and grey color for filepaths

        self.layout.addWidget(self.filenameLabel)
        self.layout.addWidget(self.filepathLabel)
        self.layout.setContentsMargins(10, 0, 0, 0)  # Remove margins if needed

        self.setLayout(self.layout)


class SearchBar(QLineEdit):
    def __init__(self, parent=None):
        super(SearchBar, self).__init__(parent)
        self.setMinimumHeight(60)  # Make the search bar taller
        font = QFont('Arial', 24)  # Larger font size for search bar text
        self.setFont(font)
        self.setPlaceholderText("   Search...")
        # Assuming parent has an 'on_search_text_changed' method
        self.textChanged.connect(parent.on_search_text_changed)
        # Set the stylesheet
        self.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid gray;
                        border-radius: 10px;
                        padding: 0 8px;
                        background: white;
                        selection-background-color: darkgray;
                    }
                """)


class SearchWindow(QWidget):
    def __init__(self, window_index: int):
        super().__init__()
        self.all_possible_results = None
        self._window_index = window_index
        self.fileSystemModel = None
        self.initUI()

    def initUI(self):
        self.all_possible_results = []     # Replace with actual search results
        self.setWindowTitle("Search Example")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        self.searchBar = SearchBar(self)
        layout.addWidget(self.searchBar)

        # Stacked layout allows to switch between different widgets in the same area
        self.stackedLayout = QStackedLayout()

        # Placeholder widget when there are no search results
        self.placeholderWidget = QLabel("")
        self.placeholderWidget.setAlignment(Qt.AlignCenter)

        # Results list for when there are search results
        self.resultsList = QListWidget(self)
        self.resultsList.setIconSize(QSize(32, 32))  # Set the size of the icons

        # Add both the placeholder and the results list to the stacked layout
        self.stackedLayout.addWidget(self.placeholderWidget)
        self.stackedLayout.addWidget(self.resultsList)

        # Start with the placeholder widget
        self.stackedLayout.setCurrentWidget(self.placeholderWidget)

        layout.addLayout(self.stackedLayout)

        self.scanButton = QPushButton("Start Scan", self)
        self.scanButton.clicked.connect(self.on_start_scan)  # Connect button click to handler
        layout.addWidget(self.scanButton)  # Add the scan button to the layout

        self.setLayout(layout)

    def on_search_text_changed(self, text):
        self.resultsList.clear()
        self.resultsList.setSpacing(4)

        if text:
            # Convert the search text to lowercase for a case-insensitive search
            search_text = text.lower()

            # Filter the results based on the search text
            filtered_results = [node for node in self.all_possible_results if search_text in node.name.lower()]

            # Show the results list if there is text
            self.stackedLayout.setCurrentWidget(self.resultsList)

            # Dictionary mapping file extensions to icon paths
            icon_paths = {
                'txt': 'ui/images/icons/txt_icon.png',
                'doc': 'ui/images/icons/word_icon.png',
                'docx': 'ui/images/icons/docx_icon.png',
                'xls': 'ui/images/icons/xls_icon.png',
                'xlsx': 'ui/images/icons/xlxs_icon.png',
                'ppt': 'ui/images/icons/ppt_icon.png',
                'pptx': 'ui/images/icons/pptx_icon.png',
                'jpeg': 'ui/images/icons/jpeg_icon.png',
                'jpg': 'ui/images/icons/image_icon.png',
                'gif': 'ui/images/icons/image_icon.png',
                'png': 'ui/images/icons/png_icon.png',
                'mp3': 'ui/images/icons/music_icon.png',
                'mp4': 'ui/images/icons/video_icon.png',
                'pdf': 'ui/images/icons/pdf_icon.png',
                'py': 'ui/images/icons/python_icon.png',
                'html': 'ui/images/icons/html_icon.png',
                'js': 'ui/images/icons/js_icon.png',
                'java': 'ui/images/icons/java_icon.png',
                'json': 'ui/images/icons/json_icon.png',
                'cpp': 'ui/images/icons/cpp_icon.png',
                'c': 'ui/images/icons/c_icon.png',
                'mov': 'ui/images/icons/mov_icon.png',
                'mkv': 'ui/images/icons/mkv_icon.png',
                'zip': 'ui/images/icons/zip_icon.png',
                'rar': 'ui/images/icons/rar_icon.png',

                # ... add more mappings as needed
            }

            for file_node in filtered_results:
                # Extract the file name and path
                file_name = file_node.name
                filepath = file_node.path

                # Check if it's a folder or if there's no file extension
                if os.path.isdir(filepath) or '.' not in filepath:
                    icon_path = 'ui/images/icons/folder_icon.png'
                else:
                    # Get the file extension and convert it to lower case
                    extension = file_node.extension().lower()[1:]
                    # Get the corresponding icon path or a default one
                    icon_path = icon_paths.get(extension, 'ui/images/icons/default_icon.png')

                item = QListWidgetItem(QIcon(QPixmap(icon_path)), "")
                fileItemWidget = FileListItem(file_name, filepath)

                # Set size hint for the item
                item_size = QSize(fileItemWidget.sizeHint().width(), fileItemWidget.sizeHint().height())
                item.setSizeHint(item_size)

                self.resultsList.addItem(item)
                self.resultsList.setItemWidget(item, fileItemWidget)

        else:
            # Show the placeholder when there is no text
            self.stackedLayout.setCurrentWidget(self.placeholderWidget)

    def on_start_scan(self):
        print("Scan started! (on separate thread)")
        threading.Thread(target=self.scan_file_system, args=(os.environ.get("SCAN_PATH"),)).start()

    def scan_file_system(self, root_path: str):
        print("SCAN PATH: ", root_path)
        FSCache = FileSystemCache()

        # if there is cache
        if FSCache.load_from_file():
            # create fileSystemModel from cache
            print('loading from cache')
            self.fileSystemModel = FSCache[root_path]

        else:
            # create model from scan path
            print('no cache found, scanning')
            if os.path.isdir(root_path):
                self.fileSystemModel = Directory(root_path, FSCache)
            else:
                raise Exception("Path given to scan was not a directory.")

        # update search results
        self.all_possible_results = [node for node in FSCache.body.values()]

        print("Scan Finished")

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
