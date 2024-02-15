from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QStackedLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

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
        self._window_index = window_index
        self.initUI()

    def initUI(self):
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
        self.resultsList.setIconSize(QSize(28, 28))  # Set the size of the icons

        # Add both the placeholder and the results list to the stacked layout
        self.stackedLayout.addWidget(self.placeholderWidget)
        self.stackedLayout.addWidget(self.resultsList)

        # Start with the placeholder widget
        self.stackedLayout.setCurrentWidget(self.placeholderWidget)

        layout.addLayout(self.stackedLayout)

        self.setLayout(layout)

    def on_search_text_changed(self, text):
        self.resultsList.clear()
        self.resultsList.setSpacing(4)  # Add some space between items for better readability
        if text:

            # Show the results list if there is text
            self.stackedLayout.setCurrentWidget(self.resultsList)

            # Example search results, replace with actual search logic - Jack working on this
            search_results = [
                'document.txt',
                'document.doc',
                'script1.py',
                'script2.py',
                'script3.py',
                'document.docx',
                'spreadsheet.xls',
                'spreadsheet.xlsx',
                'presentation.ppt',
                'presentation.pptx',
                'image.png',
                'music.mp3',
                'video.mp4',
                'pdf.pdf',
                'other_document.txt',
                'script.py',
                'script.js',
                # ... add more file types as needed
            ]

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
                # ... add more mappings as needed
            }

            # Loop through the search results
            for file_name in search_results:
                extension = file_name.split('.')[-1]  # Get the file extension
                icon_path = icon_paths.get(extension, 'ui/images/icons/default_icon.png')  # Get the corresponding icon path or a default one
                item = QListWidgetItem(QIcon(QPixmap(icon_path)), file_name)
                pixmap = QPixmap(icon_path)
                if pixmap.isNull():
                    print(f"Failed to load icon: {icon_path}")
                font = QFont('Arial', 18)
                item.setFont(font)
                self.resultsList.addItem(item)
        else:
            # Show the placeholder when there is no text
            self.stackedLayout.setCurrentWidget(self.placeholderWidget)

    def on_start_scan(self):
        # Placeholder for start scan function
        print("Scan started!")

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value