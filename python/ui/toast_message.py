from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
import python.styles.toast as t


class ToastMessage(QWidget):
    def __init__(self, message, status, parent=None):
        super(ToastMessage, self).__init__(parent)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet(self.get_style(status))

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.setGeometry(400, 400, 300, 100)  # Adjust the size and position as needed

    def show_toast(self):
        self.show()
        self.raise_()  # Bring the toast window to the front
        QTimer.singleShot(3000, self.close)  # Close the toast after 3 seconds

    @staticmethod
    def get_style(status):
        if status == 'success':
            return t.success()
        elif status == 'alert':
            return t.alert()
        elif status == 'error':
            return t.error()
        else:
            return t.info()

