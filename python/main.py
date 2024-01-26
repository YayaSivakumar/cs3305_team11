import sys
from PyQt5.QtWidgets import QApplication
from python.mainwindow import MainWindow

# Main Application (main.py):
# This script initializes and displays the main window.
# It's responsible for setting up the QApplication and starting the event loop.
def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


