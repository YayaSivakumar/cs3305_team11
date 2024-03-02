import webbrowser
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QComboBox, \
    QHBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time
import requests
from python.utils.icons import icon_paths
from PyQt5.QtWidgets import QFileDialog
import os

class FileItemWidget(QWidget):
    '''Custom widget to display a file item with an icon, filename, and remove button.'''
    # Define a signal to notify removal of a file
    removed = pyqtSignal(str)

    def __init__(self, icon_path, filename, filepath, parent=None):
        '''Initialize the widget with the icon, filename, and filepath. Also, connect the remove button to the on_remove_clicked method.'''
        super().__init__(parent)
        self.filepath = filepath
        layout = QHBoxLayout(self)

        # Create and set file icon
        iconLabel = QLabel()
        pixmap = QPixmap(icon_path)  # Use the getIconPath function to get the icon path
        print(f"icon_path: {icon_path}")
        if pixmap.isNull():
            print(f"Failed to load icon from path: {icon_path}")
        else:
            iconLabel.setPixmap(pixmap.scaled(30, 30, Qt.KeepAspectRatio))  # Adjust size as needed
        layout.addWidget(iconLabel)

        filename_label = QLabel(filename, self)
        filename_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(filename_label)

        remove_button = QPushButton(QIcon('ui/images/icons/delete_icon.png'), '', self)
        remove_button.clicked.connect(self.on_remove_clicked)
        layout.addWidget(remove_button)

        self.setLayout(layout)

    def on_remove_clicked(self):
        '''Emit the removed signal when the remove button is clicked.'''
        self.removed.emit(self.filepath)
        self.deleteLater()

class UploadThread(QThread):
    '''Custom QThread to handle file uploads and emit signals for progress and completion.'''
    finished = pyqtSignal(object)  # Emits an object instead of a string (JSON data)
    error = pyqtSignal(Exception)
    progress = pyqtSignal(int)  # Signal for progress updates
    total_progress = pyqtSignal(int)  # Signal for total progress

    def __init__(self, url, file_paths, message, persistence_hours):
        super().__init__()
        self.url = url
        self.file_paths = file_paths  # Now a list of file paths
        self.message = message
        self.persistence_hours = persistence_hours

    def run(self):
        '''Run the thread and upload the file(s).'''
        try:
            total_files = len(self.file_paths)
            for index, file_path in enumerate(self.file_paths):
                # Update total progress
                self.total_progress.emit(int((index / total_files) * 100))

                with open(file_path, 'rb') as f:
                    files = {'file': (os.path.basename(file_path), f)}
                    data = {'message': self.message, 'expiration_hours': self.persistence_hours}
                    response = requests.post(self.url, files=files, data=data)

                if response.status_code == 200:
                    response_data = response.json()
                    self.finished.emit(response_data)
                else:
                    self.error.emit(Exception(
                        f'Failed to upload file: {os.path.basename(file_path)}. Status code: {response.status_code}'))
                # Simulate upload progress for the current file
                for i in range(101):  # Simulate 0 to 100%
                    self.progress.emit(i)  # Emit progress update for current file
                    time.sleep(0.02)  # Sleep to simulate upload time

            self.total_progress.emit(100)  # Signal that overall upload is complete

        except Exception as e:
            self.error.emit(e)

class FileUploader(QWidget):
    '''Custom QWidget to handle file uploads and sharing. Emits a signal when the upload is finished.
    The signal passes the URL of the uploaded file.'''
    uploadFinished = pyqtSignal(str)  # Signal to indicate upload is finished and pass URL

    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        self.filePath = ''  # Initialize filePath
        self.folderPath = ''  # Initialize folderPath as well
        self.filePaths = []  # Initialize filePaths to hold multiple files
        self.shareable_link = ''
        self.unique_id = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Uploader')

        # Initialize the layout first
        self.layout = QVBoxLayout()

        # Continue adding other widgets to the layout
        self.label = QLabel('Select a file you wish to upload and share:')
        self.layout.addWidget(self.label)

        self.uploadButton = QPushButton('Select File')
        self.uploadButton.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.uploadButton)

        self.messageInput = QLineEdit()
        self.messageInput.setPlaceholderText('Enter a message (optional)')
        self.layout.addWidget(self.messageInput)

        self.persistenceComboBox = QComboBox()
        self.persistenceComboBox.addItems(['24 hours', '3-Days', '7-Days'])
        self.layout.addWidget(self.persistenceComboBox)

        self.selectedFileLabel = QLabel('')
        self.layout.addWidget(self.selectedFileLabel)

        # Create a layout for displaying selected files
        self.filesLayout = QVBoxLayout()
        self.layout.addLayout(self.filesLayout)

        self.uploadShareButton = QPushButton('Upload And Share Now')
        self.uploadShareButton.clicked.connect(self.uploadAndShare)
        self.layout.addWidget(self.uploadShareButton)

        # Initialize and add the progress bar to the layout
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)  # Set the maximum value to 100%
        self.layout.addWidget(self.progressBar)

        self.copyButton = QPushButton('Copy Link for sharing')
        self.copyButton.clicked.connect(self.copyLinkToClipboard)
        self.layout.addWidget(self.copyButton)
        self.copyButton.setEnabled(False)  # Initially disable the Copy to Clipboard button

        # Finally, set the layout for the widget
        self.setLayout(self.layout)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def displaySelectedFiles(self):
        '''Display the selected files in the layout.
        Also, connect the removeFile method to the removed signal of each FileItemWidget.'''
        # Clear existing file displays
        self.clearLayout(self.filesLayout)

        for file_path in self.filePaths:
            # Determine the icon based on the file extension or if it's a folder
            icon_path = self.getIconPath(file_path)
            print(f"icon_path: {icon_path}")
            # Create a FileItemWidget for each file
            file_item_widget = FileItemWidget(icon_path, os.path.basename(file_path), file_path)
            file_item_widget.removed.connect(self.removeFile)
            self.filesLayout.addWidget(file_item_widget)

    def removeFile(self, file_path):
        # Remove the file from the internal list and update the display
        if file_path in self.filePaths:
            self.filePaths.remove(file_path)
            self.displaySelectedFiles()
            self.selectedFileLabel.setText(f'Selected Files: {len(self.filePaths)} files')

    def openFileDialog(self):
        # Provide options to the user to either select files or a directory
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileOrFolderDialog = QFileDialog(self, "Select File or Folder")
        fileOrFolderDialog.setOptions(options)

        # Set file selection mode to select both files and directories
        fileOrFolderDialog.setFileMode(QFileDialog.ExistingFiles | QFileDialog.Directory)

        if fileOrFolderDialog.exec_():
            selected = fileOrFolderDialog.selectedFiles()
            # If a directory is selected, get all files within it
            if os.path.isdir(selected[0]):
                self.folderPath = selected[0]
                self.filePaths = self.get_files_from_folder(self.folderPath)
                self.selectedFileLabel.setText(f'Selected Folder: {self.folderPath}')
                self.displaySelectedFiles()
            else:
                self.filePaths = selected  # A list of selected file paths
                self.selectedFileLabel.setText(f'Selected Files: {len(self.filePaths)} files')
                self.displaySelectedFiles()

        if self.folderPath:
            self.filePaths = self.get_files_from_folder(self.folderPath)
            self.displaySelectedFiles()
            self.selectedFileLabel.setText(f'Selected Folder: {self.folderPath}')


        elif self.filePaths:
            self.displaySelectedFiles()
            self.selectedFileLabel.setText(f'Selected Files: {len(self.filePaths)} files')


    def get_files_from_folder(self, folder_path):
        file_paths = []
        for root, directories, files in os.walk(folder_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths

    def uploadAndShare(self):
        '''Upload the file(s) and share them. Also, emit the uploadFinished signal.'''
        self.progressBar.setValue(0)  # Reset progress bar
        if self.filePaths:  # This now handles both files and folders
            url = 'http://127.0.0.1:5000/upload'  # URL of the Flask app's upload endpoint
            message = self.messageInput.text()  # Extract the message from the input field
            persistence = self.persistenceComboBox.currentText()  # Extract the selected persistence option
            persistence_hours = {'24 hours': 24, '3-Days': 72, '7-Days': 168}.get(persistence, 24)

            self.uploadThread = UploadThread(url, self.filePaths, message=message, persistence_hours=persistence_hours)
            self.uploadThread.finished.connect(self.onUploadFinished)
            self.uploadThread.error.connect(self.onUploadError)
            self.uploadThread.progress.connect(lambda value: self.progressBar.setValue(value))
            self.uploadThread.total_progress.connect(lambda value: self.progressBar.setValue(value))
            self.uploadThread.start()
        else:
            self.selectedFileLabel.setText('No file or folder selected.')

    def onUploadFinished(self, response_data):
        '''Handle the upload finished and extract the URL. Also, emit the uploadFinished signal.'''
        # Handle the upload finished and extract the URL
        self.shareable_link = response_data['link']
        print(f"shareable_link: {self.shareable_link}")
        self.selectedFileLabel.setText(f'File uploaded successfully. <a href="{self.shareable_link}">Click here</a> to access the file.')
        self.selectedFileLabel.setOpenExternalLinks(True)
        self.copyButton.setEnabled(True)  # Enable the Copy to Clipboard button after link is available
        # Handle upload finished, extract URL, and emit signal
        unique_id = self.shareable_link.split('/')[-1]
        print(f"unique_id: {unique_id}")
        success_url = f"http://127.0.0.1:5000/upload_success/{unique_id}"
        self.uploadFinished.emit(success_url)
        self.progressBar.setValue(0)  # Reset or hide progress bar


    def onUploadError(self, exception):
        # Handle any errors that occurred during the upload
        self.selectedFileLabel.setText(f'Error: {str(exception)}')

    def openUploadPage(self):
        unique_id = self.shareable_link.split('/')[-1]  # Extract the unique ID from the shareable link
        url = f'http://127.0.0.1:5000/uploaded/{unique_id}'  # URL of the new splash screen
        webbrowser.open_new(url)

    # Ensure the copyLinkToClipboard method checks if shareable_link is set
    def copyLinkToClipboard(self):
        if self.shareable_link:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.shareable_link)
            self.selectedFileLabel.setText('Shareable link copied to clipboard!')
        else:
            self.selectedFileLabel.setText('No shareable link available to copy.')
        self.openUploadPage()

    def resetForm(self):
        self.filePath = ''  # Clear the selected file path
        self.messageInput.clear()  # Clear the message input field
        self.persistenceComboBox.setCurrentIndex(0)  # Reset to the first option
        self.selectedFileLabel.setText('')  # Clear the selected file label
        self.copyButton.setEnabled(False)  # Disable the Copy to Clipboard button

    def updateProgressBarStyle(self, value):

        colour = "#32CD32"  # Green

        # Calculate the gradient transition based on current progress value
        progress_percentage = value / 100

        self.progressBar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: 7px;
                text-align: center;
                background-color: #F0F0F0;
            }}

            QProgressBar::chunk {{
                background-color: {colour};
                border-radius: 5px;
                margin: 1px;
            }}
        """)

    def getIconPath(self, file_path):
        '''Return the icon path based on the file extension.
        If the file is a directory or has no extension, return the folder icon path.
        If the file has an extension, return the icon path based on the extension.'''
        print(f"file_path: {file_path}")
        if os.path.isdir(file_path) or '.' not in file_path:
            return 'ui/images/icons/folder_icon.png'
        elif '.' not in file_path:
            return 'ui/images/icons/default_icon.svg'
        else:
            extension = os.path.splitext(file_path)[1].lower()[1:]
            print(f"extension: {extension}")
            # Return the icon path based on the file extension
            return icon_paths.get(extension, 'ui/images/icons/default_icon.svg')


    @property
    def window_index(self):
        '''Return the window index.'''
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        '''Set the window index.'''
        self._window_index = value
