import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QFileDialog, QListWidgetItem, QListWidget, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QDir
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class VisualiseWindow(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        self.initUI()
    
    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout(self)

        # Create a title label
        title_label = QLabel("Visualise your folders and files")
        title_label.setFont(QFont('Arial', 24))
        title_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Create a subtitle label
        subtitle_label = QLabel("Get a visual size comparison of your folders and files\nfor quick tidying up.")
        subtitle_label.setFont(QFont('Arial', 16))
        subtitle_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Create a matplotlib canvas and add it to the layout but hide it for now
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.canvas.hide()

        # Initialize the folder_selection QComboBox
        self.folder_selection = QComboBox()
        self.folder_selection.setFont(QFont('Arial', 16))
        self.folder_selection.addItem("Your Home folder")  # Placeholder for the home folder
        self.folder_selection.addItem("Choose Folder...")  # Option to select a folder
        self.folder_selection.activated.connect(
            self.on_folder_select)  # Connect to the slot/function when an item is activated

        # Create a scan button
        scan_button = QPushButton("Explore")
        scan_button.setFont(QFont('Arial', 16))
        scan_button.setFixedSize(200, 50)  # Fixed size for the button
        scan_button.clicked.connect(self.on_scan)  # Connect to the slot/function

        # Add widgets to the layout
        self.layout.addWidget(title_label)
        self.layout.addWidget(subtitle_label)
        self.layout.addStretch()  # Add some space before the dropdown
        self.layout.addWidget(self.folder_selection)
        self.layout.addStretch()  # Add some space before the button
        self.layout.addWidget(scan_button, alignment=Qt.AlignCenter)  # Center the button horizontally

        # Create the list widget to display folder contents
        self.folder_contents = QListWidget()
        self.folder_contents.setFont(QFont('Arial', 12))

        # Styling
        self.folder_contents.setStyleSheet("""
            QListWidget {
                border: None;
                color: #333;
                background-color: #f7f7f7;
            }
            QListWidget::item {
                border-bottom: 1px solid #ddd;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #e1e1e1;
            }
        """)
        # Set the layout for the widget
        # self.setLayout(layout)

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value

    # Define the on_folder_select method
    def on_folder_select(self):
        selected_text = self.folder_selection.currentText()
        if selected_text == "Choose Folder...":
            self.select_folder()
        elif selected_text == "Your Home folder":
            self.folder_selection.setCurrentIndex(self.folder_selection.findText(os.path.expanduser('~')))

    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            # If a folder was selected, add it to the dropdown and select it
            self.folder_selection.addItem(folder_path)
            self.folder_selection.setCurrentIndex(self.folder_selection.findText(folder_path))
            # Trigger the visualization of the selected folder
            self.visualise_folder(folder_path)

    def on_scan(self):
        selected_folder = self.folder_selection.currentText()
        if selected_folder == "Choose Folder...":
            self.select_folder()
        elif selected_folder == "Your Home folder":
            home_folder_path = os.path.expanduser('~')
            self.visualise_folder(home_folder_path)
        else:
            self.visualise_folder(selected_folder)

    def visualise_folder(self, folder_path):
        file_sizes = self.calculate_folder_sizes(folder_path)
        self.visualize_sizes(file_sizes)

    def calculate_folder_sizes(self, folder_path):
        file_sizes = defaultdict(int)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    file_size = os.path.getsize(filepath)
                    _, file_extension = os.path.splitext(file)
                    if file_extension == '':
                        file_extension = 'No Extension'
                    file_sizes[file_extension] += file_size
                except FileNotFoundError:
                    continue
        return file_sizes

    def visualize_sizes(self, folder_sizes):
        # Clear the previous figure and create a new pie chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Sort the sizes to make the chart more orderly
        sorted_sizes = dict(sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True))
        
        # Data for pie chart
        labels = sorted_sizes.keys()
        sizes = sorted_sizes.values()
        
        # Make sure we have data to plot
        if not sizes:
            QMessageBox.information(self, 'No Data', 'No files to visualise in the selected directory.', QMessageBox.Ok)
            return
        
        # Explode the largest segment
        explode = [0.1 if i == 0 else 0 for i in range(len(labels))]
        
        # Plot pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
        
        # Improve readability
        for text, autotext in zip(texts, autotexts):
            text.set_fontsize(8)
            autotext.set_fontsize(8)
            autotext.set_color('white')
        
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        # Add a legend if there are too many items to label on the pie chart
        if len(labels) > 4:  # Adjust this number based on your preference
            ax.legend(wedges, labels, title="File Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Adjust layout to fit everything
        self.figure.tight_layout()
        
        # Show the canvas and draw the chart
        self.canvas.show()
        self.canvas.draw()


class FolderVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set up the user interface
        layout = QVBoxLayout()

        # Button to select folder
        self.btn_select_folder = QPushButton('Select Folder', self)
        self.btn_select_folder.clicked.connect(self.select_folder)

        # Add button to layout
        layout.addWidget(self.btn_select_folder)

        # Set the layout on the application's window
        self.setLayout(layout)

    def select_folder(self):
        # Open QFileDialog to select a folder
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        
        if folder_path:
            # Calculate folder sizes
            self.folder_sizes = self.calculate_folder_sizes(folder_path)
            # Visualize the sizes with a pie chart
            self.visualize_sizes()

    def calculate_folder_sizes(self, folder_path):
        file_sizes = defaultdict(int)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    file_size = os.path.getsize(filepath)
                    _, file_extension = os.path.splitext(file)
                    if file_extension == '':
                        file_extension = 'No Extension'
                    file_sizes[file_extension] += file_size
                except FileNotFoundError:
                    # In case a file is not found, which can happen with symlinks
                    continue
        return file_sizes

    def visualize_sizes(self, folder_sizes):
        # Clear the previous figure and create a new pie chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Sort the sizes to make the chart more orderly
        sorted_sizes = dict(sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True))
        
        # Data for pie chart
        labels = sorted_sizes.keys()
        sizes = sorted_sizes.values()
        
        # Make sure we have data to plot
        if not sizes:
            QMessageBox.information(self, 'No Data', 'No files to visualise in the selected directory.', QMessageBox.Ok)
            return
        
        # Explode the largest segment
        explode = [0.1 if i == 0 else 0 for i in range(len(labels))]
        
        # Plot pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
        
        # Improve readability
        for text, autotext in zip(texts, autotexts):
            text.set_fontsize(8)
            autotext.set_fontsize(8)
            autotext.set_color('white')
        
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        # Add a legend if there are too many items to label on the pie chart
        if len(labels) > 4:  # Adjust this number based on your preference
            ax.legend(wedges, labels, title="File Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Adjust layout to fit everything
        self.figure.tight_layout()
        
        # Show the canvas and draw the chart
        self.canvas.show()
        self.canvas.draw()