import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from collections import defaultdict
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton



class VisualiseWindow(QWidget):
    def __init__(self, window_index, fileSystemModel):
        super().__init__()
        self.fileSystemModel = fileSystemModel
        self.window_index = window_index
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # Title
        self.title = QPushButton("Visualise Window")
        self.title.setFont(QFont("Arial", 20))
        self.title.setFlat(True)

        # Add title to layout
        self.layout.addWidget(self.title)

        # Set layout
        self.setLayout(self.layout)



    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value

