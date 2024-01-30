from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class Window5(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout
        layout = QVBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("This is Window 5\n This is Video Extraction and formatting Window")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Additional labels or widgets can be added here
        layout.addWidget(QLabel("More information..."))

        layout.setAlignment(Qt.AlignCenter)  # Set alignment on the layout itself

        # Set the layout for the widget
        self.setLayout(layout)

        # Additional initialization, if necessary