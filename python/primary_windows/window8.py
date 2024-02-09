from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QComboBox

class UploadThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(Exception)

    def __init__(self, url, filePath, title, message, persistence_hours):
        super().__init__()
        self.url = url
        self.filePath = filePath
        self.message = message
        self.title = title
        self.persistence_hours = persistence_hours
        # self.password = password



    def run(self):
        try:
            with open(self.filePath, 'rb') as f:
                files = {'file': (os.path.basename(self.filePath), f)}
                data = {'message': self.message, 'title': self.title, 'expiration_hours': self.persistence_hours}
                response = requests.post(self.url, files=files, data=data)
            if response.status_code == 200:
                self.finished.emit(response.text)
            else:
                self.error.emit(Exception(f'Failed to upload file. Status code: {response.status_code}'))
        except Exception as e:
            self.error.emit(e)





class FileUploader(QWidget):
    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        # Create a layout
        layout = QVBoxLayout()
        self.filePath = ''  # Store the selected file path
        self.shareable_link = ''  # Initialize shareable_link
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Uploader')

        self.layout = QVBoxLayout()

        self.label = QLabel('Select a file you wish to upload and share:')
        self.layout.addWidget(self.label)

        self.uploadButton = QPushButton('Select File')
        self.uploadButton.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.uploadButton)

        # Title input
        self.titleInput = QLineEdit()
        self.titleInput.setPlaceholderText('Enter a title (optional)')
        self.layout.addWidget(self.titleInput)

        # Message input
        self.messageInput = QLineEdit()
        self.messageInput.setPlaceholderText('Enter a message (optional)')
        self.layout.addWidget(self.messageInput)

        # Add to your FileUploader's initUI method
        # self.passwordInput = QLineEdit()
        # self.passwordInput.setPlaceholderText('Enter a password (optional)')
        # self.passwordInput.setEchoMode(QLineEdit.Password)  # Hide password input
        # self.layout.addWidget(self.passwordInput)

        # Persistence selection
        self.persistenceComboBox = QComboBox()
        self.persistenceComboBox.addItems(['24 hours', '3-Days', '7-Days'])
        self.layout.addWidget(self.persistenceComboBox)

        # Upload and Share button
        self.uploadShareButton = QPushButton('Upload And Share Now')
        self.uploadShareButton.clicked.connect(self.uploadAndShare)
        self.layout.addWidget(self.uploadShareButton)

        self.selectedFileLabel = QLabel('')
        self.layout.addWidget(self.selectedFileLabel)

        # Add a Copy to Clipboard button
        self.copyButton = QPushButton('Copy Link for sharing')
        self.copyButton.clicked.connect(self.copyLinkToClipboard)
        self.layout.addWidget(self.copyButton)

        # Ensure the Copy to Clipboard button is initially disabled
        self.copyButton.setEnabled(False)

        self.setLayout(self.layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*);;Python Files (*.py)", options=options)
        if self.filePath:
            self.selectedFileLabel.setText(f'Selected File: {self.filePath}')

    def uploadAndShare(self):
        if self.filePath:
            url = 'http://127.0.0.1:5000/upload'
            title = self.titleInput.text()  # Make sure to retrieve the title from the input field
            message = self.messageInput.text()
            persistence = self.persistenceComboBox.currentText()
            persistence_hours = {'24 hours': 24, '3-Days': 72, '7-Days': 168}.get(persistence,
                                                                                  24)  # Corrected the dictionary keys to match the combobox items
            # password = self.passwordInput.text()

            # Correctly passing the 'title' argument now
            self.uploadThread = UploadThread(url, self.filePath, title, message, persistence_hours)
            self.uploadThread.finished.connect(self.onUploadFinished)
            self.uploadThread.error.connect(self.onUploadError)
            self.uploadThread.start()
        else:
            self.selectedFileLabel.setText('No file selected.')

    def onUploadFinished(self, response_text):
        # Assume response_text contains the full message with the link
        # Extract just the URL part if necessary
        shareable_link = response_text.split(': ')[-1].strip()  # Adjust parsing as needed
        self.shareable_link = shareable_link  # Ensure this is set
        self.selectedFileLabel.setText(f'File uploaded successfully. <a href="{shareable_link}">Click here</a> to access the file.')
        self.selectedFileLabel.setOpenExternalLinks(True)
        self.copyButton.setEnabled(True)  # Enable the Copy to Clipboard button after link is available


    def onUploadError(self, exception):
        # Handle any errors that occurred during the upload
        self.selectedFileLabel.setText(f'Error: {str(exception)}')


    def uploadFile(self, filePath):
        url = 'http://127.0.0.1:5000/upload'  # URL of the Flask app's upload endpoint
        message = self.messageInput.text()
        persistence = self.persistenceComboBox.currentText()
        # Convert persistence option to hours for the backend
        persistence_hours = {'1-Day': 24, '3-Days': 72, '7-Days': 168}.get(persistence, 24)
        try:
            with open(filePath, 'rb') as f:
                files = {'file': (os.path.basename(filePath), f)}
                data = {'message': message, 'expiration_hours': persistence_hours}
                response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(response.text)

                # Split the response text and get the last part, assuming the format is consistent
                shareable_link = response.text.split(': ')[-1]
                self.selectedFileLabel.setText(f'File uploaded successfully. <a href="{shareable_link}">Click here</a> to access the file.')
                self.selectedFileLabel.setOpenExternalLinks(True)
                self.copyButton.setEnabled(True)  # Enable the Copy to Clipboard button after link is available

            else:
                self.selectedFileLabel.setText(f'Failed to upload file. Status code: {response.status_code}')
        except Exception as e:
            self.selectedFileLabel.setText(f'Error: {str(e)}')
        finally:
            self.filePath = ''  # Reset the file path after uploading

    # Ensure the copyLinkToClipboard method checks if shareable_link is set
    def copyLinkToClipboard(self):
        if self.shareable_link:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.shareable_link)
            self.selectedFileLabel.setText('Shareable link copied to clipboard!')
        else:
            self.selectedFileLabel.setText('No shareable link available to copy.')

    def resetForm(self):
        self.filePath = ''  # Clear the selected file path
        self.messageInput.clear()  # Clear the message input field
        self.persistenceComboBox.setCurrentIndex(0)  # Reset to the first option
        self.selectedFileLabel.setText('')  # Clear the selected file label
        self.copyButton.setEnabled(False)  # Disable the Copy to Clipboard button

    # Call this method at the end of onUploadFinished and onUploadError




    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
