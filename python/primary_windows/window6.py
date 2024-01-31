from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Window6(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        # Create a layout
        layout = QVBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("This is Window 6")
        layout.addWidget(label)

        # Additional labels or widgets can be added here
        layout.addWidget(QLabel("More information..."))

        # Set the layout for the widget
        self.setLayout(layout)

        # Additional initialization, if necessary

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
