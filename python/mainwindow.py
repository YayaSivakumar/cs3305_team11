import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QAction

from python.primary_windows.window1 import Window1
from python.primary_windows.window2 import Window2
from python.primary_windows.window3 import Window3
from python.primary_windows.window4 import Window4
from python.primary_windows.window5 import Window5
from python.primary_windows.window6 import Window6
from python.primary_windows.window7 import Window7
from python.primary_windows.welcome_window import WelcomeWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

         # Set the main window's title and initial size
        self.setWindowTitle("Main Window with Sidebar")
        self.setGeometry(100, 100, 1000, 600)

        # Create the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Create the sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # Create the different screens
        self.welcome_window = WelcomeWindow()
        self.window1 = Window1()
        self.window2 = Window2()
        self.window3 = Window3()
        self.window4 = Window4()
        self.window5 = Window5()
        self.window6 = Window6()
        self.window7 = Window7()

        # Add the sidebar to the main layout
        self.main_layout.addWidget(self.sidebar, 2)  # 1/5th of the space for the sidebar

        # Create a stacked widget to hold the different screens
        self.stacked_widget = QStackedWidget()


        # Add windows to the stacked widget
        self.stacked_widget.addWidget(self.welcome_window)
        self.stacked_widget.addWidget(self.window1)
        self.stacked_widget.addWidget(self.window2)
        self.stacked_widget.addWidget(self.window3)
        self.stacked_widget.addWidget(self.window4)
        self.stacked_widget.addWidget(self.window5)
        self.stacked_widget.addWidget(self.window6)
        self.stacked_widget.addWidget(self.window7)



        # Add the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget, 8)  # Adjusting space for main content

        # Add buttons to the sidebar
        button_1_file_explorer = QPushButton(f"File Explorer")
        button_1_file_explorer.clicked.connect(self.show_window1)
        self.sidebar_layout.addWidget(button_1_file_explorer)

        # Add buttons to the sidebar
        button_2_music = QPushButton(f"Music Explorer")
        button_2_music.clicked.connect(self.show_window2)
        self.sidebar_layout.addWidget(button_2_music)

        # Add buttons to the sidebar
        button_3_pdf_explorer = QPushButton(f"PDFDocument Explorer")
        button_3_pdf_explorer.clicked.connect(self.show_window3)
        self.sidebar_layout.addWidget(button_3_pdf_explorer)

        # Add buttons to the sidebar
        button_4_image_explorer = QPushButton(f"Image Explorer")
        button_4_image_explorer.clicked.connect(self.show_window4)
        self.sidebar_layout.addWidget(button_4_image_explorer)

        # Add buttons to the sidebar
        button_5_video_explorer = QPushButton(f"Video Explorer")
        button_5_video_explorer.clicked.connect(self.show_window5)
        self.sidebar_layout.addWidget(button_5_video_explorer)

        # Add buttons to the sidebar
        button_6_file_shredder = QPushButton(f"Shredder")
        button_6_file_shredder.clicked.connect(self.show_window6)
        self.sidebar_layout.addWidget(button_6_file_shredder)

        # Add buttons to the sidebar
        button_7_visualise = QPushButton(f"Visualise")
        button_7_visualise.clicked.connect(self.show_window7)
        self.sidebar_layout.addWidget(button_7_visualise)

        # Set the default screen to the welcome window
        self.stacked_widget.setCurrentIndex(0)




    def show_window1(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_window2(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_window3(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_window4(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_window5(self):
        self.stacked_widget.setCurrentIndex(5)

    def show_window6(self):
        self.stacked_widget.setCurrentIndex(6)

    def show_window7(self):
        self.stacked_widget.setCurrentIndex(7)

    def apply_stylesheet(self):
            style = """
            QMainWindow {
                background-color: #F5F5F5;
            }
            QPushButton {
                border: 2px solid #8F8F8F;
                border-radius: 10px;
                background-color: #E0E0E0;
                padding: 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                border-color: #3daee9;
                background-color: #AEE0E0;
            }
            """
            self.setStyleSheet(style)



    def createMenuBar(self):
        menuBar = self.menuBar()

        # File menu
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)

        viewMenu = menuBar.addMenu("View")
        viewMenu.addAction(self.showFilesAction)
        appearanceMenu = viewMenu.addMenu("Appearance")
        appearanceMenu.addAction(self.toggleDarkModeAction)

    def create_actions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("New")
        # Creating actions using the second constructor
        self.openAction = QAction("Open...", self)
        self.saveAction = QAction("Save", self)
        self.exitAction = QAction("Exit", self)

        self.undoAction = QAction("Undo", self)
        self.undoAction.triggered.connect(self.undo_action)


        self.redoAction = QAction("Redo", self)
        self.redoAction.triggered.connect(self.redo_action)

        self.helpContentAction = QAction("Help Content", self)
        self.aboutAction = QAction("About", self)

        self.appearanceAction = QAction("Appearance", self)
        self.showFilesAction = QAction("Show Files", self)
        self.toggleDarkModeAction = QAction("Toggle Dark Mode", self)
        self.toggleDarkModeAction.triggered.connect(self.toggleDarkMode)

    def undo_action(self):
        self.undoAction.setEnabled(False)
#       Call to backend function

    def redo_action(self):
        self.redoAction.setEnabled(False)
#       Call to backend function

    def createMenuBar(self):
        menuBar = self.menuBar()

        # File menu
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)

        viewMenu = menuBar.addMenu("View")
        viewMenu.addAction(self.showFilesAction)
        appearanceMenu = viewMenu.addMenu("Appearance")
        appearanceMenu.addAction(self.toggleDarkModeAction)

    def create_actions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("New")
        # Creating actions using the second constructor
        self.openAction = QAction("Open...", self)
        self.saveAction = QAction("Save", self)
        self.exitAction = QAction("Exit", self)

        self.undoAction = QAction("Undo", self)
        self.undoAction.triggered.connect(self.undo_action)


        self.redoAction = QAction("Redo", self)
        self.redoAction.triggered.connect(self.redo_action)

        self.helpContentAction = QAction("Help Content", self)
        self.aboutAction = QAction("About", self)

        self.appearanceAction = QAction("Appearance", self)
        self.showFilesAction = QAction("Show Files", self)
        self.toggleDarkModeAction = QAction("Toggle Dark Mode", self)
        self.toggleDarkModeAction.triggered.connect(self.toggleDarkMode)

    def undo_action(self):
        self.undoAction.setEnabled(False)
#       Call to backend function

    def redo_action(self):
        self.redoAction.setEnabled(False)
#       Call to backend function