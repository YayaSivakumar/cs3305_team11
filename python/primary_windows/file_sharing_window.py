import webbrowser

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QComboBox, \
    QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, time
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QLineEdit, QComboBox

class UploadThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(Exception)
    progress = pyqtSignal(int)  # Add a signal for progress updates

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
            # Simulate upload progress
            for i in range(101):  # Simulate 0 to 100%
                self.progress.emit(i)  # Emit progress update
                time.sleep(0.02)  # Sleep to simulate upload time
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
    uploadFinished = pyqtSignal(str)  # Signal to indicate upload is finished and pass URL

    def __init__(self, window_index):
        super().__init__()
        self.window_index = window_index
        self.filePath = ''  # Store the selected file path
        self.shareable_link = ''  # Initialize shareable_link
        self.unique_id = ''  # Initialize unique_id
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

        self.titleInput = QLineEdit()
        self.titleInput.setPlaceholderText('Enter a title (optional)')
        self.layout.addWidget(self.titleInput)

        self.messageInput = QLineEdit()
        self.messageInput.setPlaceholderText('Enter a message (optional)')
        self.layout.addWidget(self.messageInput)

        self.persistenceComboBox = QComboBox()
        self.persistenceComboBox.addItems(['24 hours', '3-Days', '7-Days'])
        self.layout.addWidget(self.persistenceComboBox)

        self.uploadShareButton = QPushButton('Upload And Share Now')
        self.uploadShareButton.clicked.connect(self.uploadAndShare)
        self.layout.addWidget(self.uploadShareButton)

        # Initialize and add the progress bar to the layout
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)  # Set the maximum value to 100%
        self.layout.addWidget(self.progressBar)

        self.selectedFileLabel = QLabel('')
        self.layout.addWidget(self.selectedFileLabel)

        self.copyButton = QPushButton('Copy Link for sharing')
        self.copyButton.clicked.connect(self.copyLinkToClipboard)
        self.layout.addWidget(self.copyButton)
        self.copyButton.setEnabled(False)  # Initially disable the Copy to Clipboard button

        # Finally, set the layout for the widget
        self.setLayout(self.layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*);;Python Files (*.py)", options=options)
        if self.filePath:
            self.selectedFileLabel.setText(f'Selected File: {self.filePath}')

    def uploadAndShare(self):
        self.progressBar.setValue(0)  # Reset progress bar
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

            # Connect progress signal to both update the value and dynamically style the progress bar
            self.uploadThread.progress.connect(lambda value: self.progressBar.setValue(value))
            self.uploadThread.progress.connect(self.updateProgressBarStyle)

            self.uploadThread.start()
        else:
            self.selectedFileLabel.setText('No file selected.')

    def onUploadFinished(self):
        # Extract the shareable link from the response text
        print(f"shareable_link: {self.shareable_link}")
        self.shareable_link = self.shareable_link  # Ensure this is set
        self.selectedFileLabel.setText(f'File uploaded successfully. <a href="{self.shareable_link}">Click here</a> to access the file.')
        self.selectedFileLabel.setOpenExternalLinks(True)
        self.copyButton.setEnabled(True)  # Enable the Copy to Clipboard button after link is available
        # Handle upload finished, extract URL, and emit signal
        unique_id = self.shareable_link.split('/')[-1]
        print(f"unique_id: {unique_id}")
        success_url = f"http://127.0.0.1:5000/upload/success/{unique_id}"
        self.uploadFinished.emit(success_url)
        self.progressBar.setValue(0)  # Reset or hide progress bar



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
                print(f'Response {response}')
                print(f'Response Text{response.text}')

                response_json = response.json()
                print(f'Response JSON{response_json}')
                self.shareable_link = response_json['link']
                print(f'Shareable Link {self.shareable_link}')
                self.selectedFileLabel.setText(f'File uploaded successfully. <a href="{self.shareable_link}">Click here</a> to access the file.')
                self.selectedFileLabel.setOpenExternalLinks(True)
                self.copyButton.setEnabled(True)  # Enable the Copy to Clipboard button after link is available

            else:
                self.selectedFileLabel.setText(f'Failed to upload file. Status code: {response.status_code}')
        except Exception as e:
            self.selectedFileLabel.setText(f'Error: {str(e)}')
        finally:
            self.filePath = ''  # Reset the file path after uploading

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

    @property
    def window_index(self):
        return self._window_index

    @window_index.setter
    def window_index(self, value):
        self._window_index = value
