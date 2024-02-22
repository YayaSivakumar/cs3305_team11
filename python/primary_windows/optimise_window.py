from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QWidget, QTabWidget, QColumnView, QHBoxLayout, QPushButton, QSplitter, QVBoxLayout, QMessageBox

from python.ui.drag_drop import *
from python.ui.custom_file_system_model import *

from python.modules.compress import compress
from python.modules.deduplicate import deduplicate
# from python.modules.scheduler import scheduler


class OptimiseWindow(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        self.duplicate_files = []

        # Create a tab widgets
        self.tabs = QTabWidget()
        self._compression_tab = QWidget()
        self._deduplication_tab = QWidget()
        self._scheduling_tab = QWidget()

        # Create a layout
        self.layout = QVBoxLayout()

        # Add tabs
        self.tabs.addTab(self._compression_tab, "Compression")
        self.tabs.addTab(self._deduplication_tab, "Deduplication")
        self.tabs.addTab(self._scheduling_tab, "Scheduling")
        self.tabs.setStyleSheet("""
        QTabBar::tab {
            background: lightgray;
            width: 200px;
            padding: 10px;
            border: 1px solid #C4C4C3;
            border-bottom-color: #C2C7CB;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                        stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }
        QTabWidget::pane { 
            border-top: 2px solid #C2C7CB;
        }
        """)

        # Compression tab layout
        self.tab1Layout = QHBoxLayout()

        # Initialize the model for the ColumnView
        self.model = CustomFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        # Set up the ColumnView
        self.column_view = QColumnView()
        self.column_view.setModel(self.model)
        self.column_view.setRootIndex(self.model.index(os.path.expanduser('~')))

        # Create the dragDropLabel
        self.dragDropLabel = CircularDragDropLabel()

        # Create a description label
        compression_description_label = QLabel(
            "Select file or directory for compression. Types:\n"
            "Image: (jpeg, jpg, HEIC)\n"
            "Video: (mp4, mov, avi)\n"
            "Audio: (wav, mp3, aac)\n"
            "Documents: (pdf, docx, doc)")
        compression_description_label.setWordWrap(True)
        compression_description_label.setAlignment(Qt.AlignTop)  # Align the text to the top

        # Add a button to trigger file organization
        self.compressButton = QPushButton("Compress")
        self.compressButton.clicked.connect(self.onCompressClicked)

        # Create a QVBoxLayout for the description label, compress button, and dragDropLabel
        self.tab1_right_layout = QVBoxLayout()
        self.tab1_right_layout.addWidget(compression_description_label)  # Add the description label to the layout
        self.tab1_right_layout.addWidget(self.dragDropLabel)
        self.tab1_right_layout.addWidget(self.compressButton)
        self.tab1_right_layout.addStretch()

        # Add the column view and the VBox to the tab layout
        self.tab1Layout.addWidget(self.column_view)
        self.tab1Layout.addLayout(self.tab1_right_layout)

        self._compression_tab.setLayout(self.tab1Layout)

        # Deduplication layout
        self.tab2Layout = QHBoxLayout()

        # Create a description label
        deduplication_description_label = QLabel(
            "Select a Directory for processing, returns list of paths for all duplicate files)")
        deduplication_description_label.setWordWrap(True)
        deduplication_description_label.setAlignment(Qt.AlignTop)  # Align the text to the top

        # Add a button to trigger file organization
        self.deduplicationButton = QPushButton("De-Duplicate")
        self.deduplicationButton.clicked.connect(self.onDeDuplicateClicked)

        # Initialize the model for the ColumnView
        self.model2 = CustomFileSystemModel()
        self.model2.setRootPath(QDir.currentPath())
        self.model2.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        # Set up the ColumnView
        self.column_view2 = QColumnView()
        self.column_view2.setModel(self.model2)
        self.column_view2.setRootIndex(self.model2.index(os.path.expanduser('~')))

        # Create the dragDropLabel
        self.dragDropLabel2 = CircularDragDropLabel()

        # Create a QVBoxLayout for the description label, compress button, and dragDropLabel
        self.tab2_right_layout = QVBoxLayout()
        self.tab2_right_layout.addWidget(deduplication_description_label)  # Add the description label to the layout
        self.tab2_right_layout.addWidget(self.dragDropLabel2)
        self.tab2_right_layout.addWidget(self.deduplicationButton)
        self.tab2_right_layout.addStretch()

        # Add the column view and the VBox to the tab layout
        self.tab2Layout.addWidget(self.column_view2)
        self.tab2Layout.addLayout(self.tab2_right_layout)

        self._deduplication_tab.setLayout(self.tab2Layout)

        # Scheduling layout
        self.tab3Layout = QVBoxLayout()
        self.tab3Label = QLabel("Scheduling Settings Here")
        self.tab3Layout.addWidget(self.tab3Label)
        self._scheduling_tab.setLayout(self.tab3Layout)

        # Add tabs to main layout
        self.layout.addWidget(self.tabs)

        # Set the layout for the widget
        self.setLayout(self.layout)

    def onCompressClicked(self):
        paths_to_compress = []

        # Check if there are files dropped in drag-and-drop area
        if self.dragDropLabel.droppedFiles:
            paths_to_compress.extend(self.dragDropLabel.droppedFiles)

        # Check if there is a selection in the tree view
        elif self.column_view.currentIndex().isValid():
            tree_view_path = self.model.filePath(self.column_view.currentIndex())
            if tree_view_path:
                paths_to_compress.append(tree_view_path)

        # If there are paths selected
        if paths_to_compress:
            message = f"Do you want to organize the following items?\n\n" + "\n".join(paths_to_compress)
            reply = QMessageBox.question(self, 'Organize Confirmation', message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                for path in paths_to_compress:
                    path_to_new_file = compress(path)
                    QMessageBox.information(self, 'Success',
                                            f'Created: {path_to_new_file}',
                                            QMessageBox.Ok)

        else:
            QMessageBox.information(self, 'No Selection',
                                    'Please select a file or folder from the tree view or drag and drop files.',
                                    QMessageBox.Ok)

    def onDeDuplicateClicked(self):
        paths_to_deduplicate = []

        # Check if there are files dropped in drag-and-drop area
        if self.dragDropLabel2.droppedFiles:
            paths_to_deduplicate.extend(self.dragDropLabel2.droppedFiles)

        # Check if there is a selection in the tree view
        elif self.column_view2.currentIndex().isValid():
            tree_view_path = self.model.filePath(self.column_view2.currentIndex())
            if tree_view_path:
                paths_to_deduplicate.append(tree_view_path)

        # If there are paths selected
        if paths_to_deduplicate:
            message = f"Do you want to optimise the following items?\n\n" + "\n".join(paths_to_deduplicate)
            reply = QMessageBox.question(self, 'Organize Confirmation', message, QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)

            if reply == QMessageBox.Yes:
                for path in paths_to_deduplicate:
                    self.duplicate_files = deduplicate(path)
                    if self.duplicate_files:
                        QMessageBox.information(self, 'Success',
                                                f'The following files are duplicates: {self.duplicate_files}',
                                                QMessageBox.Ok)
                    else:
                        QMessageBox.information(self, 'Success',
                                                f'No duplicates found in {path}.',
                                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, 'No Selection',
                                    'Please select a file or folder from the tree view or drag and drop files.',
                                    QMessageBox.Ok)

    def onScheduleSelected(self):
        pass

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
