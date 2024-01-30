import sys
from PyQt5.QtWidgets import QApplication
from python.mainwindow import MainWindow

def main():
    '''Main application event loop. This script initializes and displays the main window.
    It's responsible for setting up the QApplication and starting the event loop.'''
    app = QApplication(sys.argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


