import os
from PyQt5.QtCore import Qt, QEvent, QDir
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtWidgets import QComboBox, QLabel, QListWidget, QMessageBox

from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go


class PlotlyWidget(QWebEngineView):
    def __init__(self, figure, parent=None):
        super().__init__(parent)
        self.figure = figure
        self.setFigure(figure)

    def setFigure(self, figure):
        if figure is not None:
            html_content = figure.to_html(full_html=False, include_plotlyjs='cdn')
            self.setHtml(html_content)
            # Save the HTML to a file for debugging
            with open("debug_plotly_chart.html", "w") as f:
                f.write(html_content)
        else:
            self.setHtml("")  # Clear the view if no figure is provided


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

        # Instead of creating a Figure and FigureCanvas, create a PlotlyWidget
        self.plotly_widget = PlotlyWidget(None)
        self.layout.addWidget(self.plotly_widget)
        self.plotly_widget.hide()

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
        labels, parents, values = self.calculate_directory_structure(folder_path)
        self.visualize_sizes(labels, parents, values)

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

    def visualize_sizes(self, labels, parents, values):
        if not labels:
            QMessageBox.information(self, 'No Data', 'No files to visualise in the selected directory.', QMessageBox.Ok)
            return

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
        ))
        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        self.plotly_widget.setFigure(fig)
        self.plotly_widget.show()

    def calculate_directory_structure(self, folder_path):
        labels = ['Root']  # Starting with 'Root' as the base label
        parents = ['']  # Root has no parent
        values = [0]  # Initialize with zero; will recalculate later

        for root, dirs, files in os.walk(folder_path, topdown=True):
            for name in dirs + files:  # Iterate over directories and files together
                current_path = os.path.join(root, name)
                size = sum(os.path.getsize(os.path.join(dirpath, filename))
                           for dirpath, dirnames, filenames in os.walk(current_path)
                           for filename in filenames) if os.path.isdir(current_path) else os.path.getsize(current_path)
                labels.append(name)
                parent_label = 'Root' if root == folder_path else os.path.basename(root)
                parents.append(parent_label)
                values.append(size)

        # Update the size of the root based on the sizes of its immediate children
        root_size = sum(size for size, parent in zip(values[1:], parents[1:]) if parent == 'Root')
        values[0] = root_size

        print("Labels:", labels)
        print("Parents:", parents)
        print("Values:", values)

        return labels, parents, values


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