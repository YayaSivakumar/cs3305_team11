import sys
from PyQt5.QtWidgets import QApplication
from python.mainwindow import MainWindow
from python.splash_window import SplashWindow


def main():
    """Main application event loop. This script initializes and displays the main window.
    It's responsible for setting up the QApplication and starting the event loop."""
    app = QApplication(sys.argv)
    splash = SplashWindow()
    splash.fileSystemModelReady.connect(init_main_window)
    splash.show()
    sys.exit(app.exec_())


def init_main_window(model):
    print("FileSystemModel Path:\t", model.path)
    main_window: MainWindow = MainWindow(model)
    main_window.show()


if __name__ == '__main__':
    main()
