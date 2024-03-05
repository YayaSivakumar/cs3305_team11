import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from collections import defaultdict
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QLabel, QListWidget, QMessageBox

from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go

import python.model.FileSystemNodeModel


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
    def __init__(self, window_index, fileSystemModel):
        super().__init__()
        self.fileSystemModel = fileSystemModel
        self.window_index = window_index
        self.initUI()
        self.visualise_folder()

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

        self.visualise_folder()
        self.setLayout(self.layout)

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value

    def setFileSystemModel(self, fileSystemModel):
        self.fileSystemModel = fileSystemModel
        self.updateVisualization()  # Update the visualization whenever the model is set

    def updateVisualization(self):
        # Here, we assume that your fileSystemModel object has a method that returns
        # the folder path. You will need to replace 'getFolderPath' with the actual method name.
        folder_path = self.fileSystemModel.path

        # Now, use 'folder_path' to calculate the directory structure and visualize it
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

        self.plotly_widget.setFigure(fig) # Update the figure in the PlotlyWidget
        self.plotly_widget.show()  # Make sure the widget is shown

    # Updated method to accept folder_path
    def calculate_directory_structure(self):
        labels = ['Root']
        parents = ['']
        values = [0]

        # Here, traverse your FileSystemNodeModel to get the structure
        # This part needs to be implemented based on how FileSystemNodeModel works
        # The following is just an illustrative placeholder
        print("Calculating sizes...")
        nodes = self.fileSystemModel.calculate_folder_size()
        other_size = 0
        for node in nodes:
            if type(node) != python.model.FileSystemNodeModel.Directory:
                other_size += node.size
            else:
                labels.append(node.name)
                parents.append(node.parent.name if node.parent else 'Root')
                values.append(node.size)
        labels.append('Other')
        values.append(other_size)
        parents.append('Root')
        # Recalculate the root size based on children
        root_size = sum(values[1:])
        values[0] = root_size

        return labels, parents, values

    def visualise_folder(self):
        labels, parents, values = self.calculate_directory_structure()
        self.visualize_sizes(labels, parents, values)