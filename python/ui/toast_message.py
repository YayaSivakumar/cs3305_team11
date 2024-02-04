# toast_message.py
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from python.styles.toast import ToastStyle, SuccessStyle, AlertStyle, ErrorStyle, InfoStyle


class ToastMessage(QWidget):
    def __init__(self, message, status, timeout=True, opacity=1.0, font_size=12, parent=None):
        super(ToastMessage, self).__init__(parent)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)

        self.timeout = timeout

        # Select the appropriate style based on the status
        style_classes = {
            'success': SuccessStyle(opacity=opacity, font_size=font_size),
            'alert': AlertStyle(opacity=opacity, font_size=font_size),
            'error': ErrorStyle(opacity=opacity, font_size=font_size),
        }
        selected_style_class = style_classes.get(status, InfoStyle(opacity=opacity, font_size=font_size))

        # Instantiate the style class and get the styles
        self.style = selected_style_class.get_main_style() + selected_style_class.get_style()
        self.setStyleSheet(self.style)

        layout = QVBoxLayout(self)
        if not self.timeout:
            close_button = self.create_close_button()
            layout.addWidget(close_button)
            layout.addWidget(self.label)
        else:
            layout.addWidget(self.label)
            QTimer.singleShot(3000, self.close)  # Close the toast after 3 seconds

        self.setGeometry(400, 400, 300, 100)  # Adjust the size and position as needed

    def create_close_button(self):
        close_button = QPushButton("x", self)
        close_button.clicked.connect(self.close)
        return close_button

    def show_toast(self):
        self.show()
        self.raise_()  # Bring the toast window to the front

