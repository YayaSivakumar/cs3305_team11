# toast_message.py
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout
from python.styles.toast import SuccessStyle, AlertStyle, ErrorStyle, InfoStyle


class ToastMessage(QPushButton):
    def __init__(self, message, status, timeout=True, opacity=1.0, font_size=12, parent=None):
        super(ToastMessage, self).__init__(message, parent)

        # Select the appropriate style based on the status
        style_classes = {
            'success': SuccessStyle(),
            'alert': AlertStyle(),
            'error': ErrorStyle(),
        }
        self.selected_style_class = style_classes.get(status, InfoStyle())

        # Instantiate the style class and get the styles
        self.style = self.selected_style_class.get_main_style() + self.selected_style_class.get_style()
        self.setStyleSheet(self.style)

        self.setGeometry(400, 400, 200, 70)  # Adjust the size and position as needed
        self.clicked.connect(self.hide)

    def show_toast(self):
        self.show()
        self.raise_()  # Bring the toast window to the front


