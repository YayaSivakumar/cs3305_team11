from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class Window4(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        # Create a layout
        layout = QVBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("This is Window 4\n IMAGE EXPLORER")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Additional labels or widgets can be added here
        layout.addWidget(QLabel("More information..."))

        layout.setAlignment(Qt.AlignCenter)  # Set alignment on the layout itself

        # Set the layout for the widget
        self.setLayout(layout)

        # Additional initialization, if necessary

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
