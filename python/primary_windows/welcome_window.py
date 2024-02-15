from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QListWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WelcomeWindow(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self._window_index = window_index
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        title_label = QLabel("Welcome to your File Explorer and Organiser")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))

        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.on_search_text_changed)

        subtitle_label = QLabel("Start with thorough scan of your drive, folders and files.")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont('Arial', 14))

        start_scan_button = QPushButton("Start Scan")
        start_scan_button.setFont(QFont('Arial', 14))
        start_scan_button.clicked.connect(self.on_start_scan)

        self.resultsList = QListWidget(self)

        layout.addStretch(1)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(self.searchBar)
        layout.addWidget(self.resultsList)
        layout.addStretch(1)
        layout.addWidget(start_scan_button, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)

    def on_start_scan(self):
        print("Scan started!")

    def on_search_text_changed(self, text):
        self.resultsList.clear()
        if text:
            self.resultsList.addItem(f"Result for {text}")
            self.resultsList.addItem(f"Another result for {text}")

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
