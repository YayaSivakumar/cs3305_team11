from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class WelcomeWindow(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        self.initUI()

    def initUI(self):
        # Main layout of the window
        layout = QVBoxLayout(self)

        # Create a QLabel for the title
        title_label = QLabel("Welcome to your File Explorer and Organiser")
        title_label.setAlignment(Qt.AlignCenter)  # Center the text horizontally
        title_label.setFont(QFont('Arial', 24, QFont.Bold))  # Set font and size

        # Create a QLabel for the subtitle
        subtitle_label = QLabel("Start with thorough scan of your drive, folders and files.")
        subtitle_label.setAlignment(Qt.AlignCenter)  # Center the text horizontally
        subtitle_label.setFont(QFont('Arial', 14))  # Set font and size

        # Create a QPushButton for the action
        start_scan_button = QPushButton("Start Scan")
        start_scan_button.setFont(QFont('Arial', 14))  # Set font and size

        # Add widgets to the layout with stretch to center them vertically
        layout.addStretch(1)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addStretch(1)
        layout.addWidget(start_scan_button, alignment=Qt.AlignCenter)  # Center the button horizontally
        layout.addStretch(1)

        # Set the main layout of the widget
        self.setLayout(layout)

    def on_start_scan(self):
        # Placeholder for start scan function
        print("Scan started!")

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
