# toast_message.py

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from python.styles.toast import ToastStyle, SuccessStyle, AlertStyle, ErrorStyle, InfoStyle


class ToastMessage(QWidget):
    def __init__(self, message, status, opacity=1.0, font_size=12, parent=None):
        super(ToastMessage, self).__init__(parent)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)

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
        layout.addWidget(self.label)

        self.setGeometry(400, 400, 300, 100)  # Adjust the size and position as needed

    def show_toast(self):
        self.show()
        self.raise_()  # Bring the toast window to the front
        QTimer.singleShot(3000, self.close)  # Close the toast after 3 seconds
