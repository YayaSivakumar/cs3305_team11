from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Window3(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        # Create a layout
        layout = QVBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("This is Window 3\n This is PDF Extraction and formatting Window")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Additional label with center alignment
        info_label = QLabel("More information...")
        info_label.setAlignment(Qt.AlignCenter)  # Set alignment on the label
        layout.addWidget(info_label)

        # Set the layout for the widget
        self.setLayout(layout)

        # Additional initialization, if necessary

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value