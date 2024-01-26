from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel


class CircularDragDropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drag and drop files here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #aaa;
            }
        ''')
        self.setFixedSize(200, 200)  # Fixed size for circle
        self.setAcceptDrops(True)
        self.droppedFiles = []  # List to store the paths of the dropped files

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.droppedFiles = [u.toLocalFile() for u in event.mimeData().urls()]
        self.setText("\n".join(self.droppedFiles))
        print(self.droppedFiles)

    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        path.addEllipse(0, 0, 200, 200)
        painter.setClipPath(path)
        super().paintEvent(event)
