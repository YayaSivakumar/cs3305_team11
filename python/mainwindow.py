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
import styles.system_theme
import styles.sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the main window's title and initial size
        self.setWindowTitle("Main Window with Sidebar")
        self.setGeometry(100, 100, 1000, 600)

        # Create actions
        self.create_actions()
        self.createMenuBar()

        # System Theme & Dark Mode Boolean
        self.dark_mode = False
        self.apply_system_theme(self.dark_mode)

        # Create the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Create the sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # Create the different screens
        self.welcome_window = WelcomeWindow(0)
        self.window1 = Window1(1)
        self.window2 = Window2(2)
        self.window3 = Window3(3)
        self.window4 = Window4(4)
        self.window5 = Window5(5)
        self.window6 = Window6(6)
        self.window7 = Window7(7)



        # Add the sidebar to the main layout
        self.main_layout.addWidget(self.sidebar, 2)  # 2/10 of the space for the sidebar

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
        button_1_file_explorer.clicked.connect(lambda: self.show_window(self.window1.window_index))
        self.sidebar_layout.addWidget(button_1_file_explorer)

        # Add buttons to the sidebar
        button_2_music = QPushButton(f"Music Explorer")
        button_2_music.clicked.connect(lambda: self.show_window(self.window2.window_index))
        self.sidebar_layout.addWidget(button_2_music)

        # Add buttons to the sidebar
        button_3_pdf_explorer = QPushButton(f"PDFDocument Explorer")
        button_3_pdf_explorer.clicked.connect(lambda: self.show_window(self.window3.window_index))
        self.sidebar_layout.addWidget(button_3_pdf_explorer)

        # Add buttons to the sidebar
        button_4_image_explorer = QPushButton(f"Image Explorer")
        button_4_image_explorer.clicked.connect(lambda: self.show_window(self.window4.window_index))
        self.sidebar_layout.addWidget(button_4_image_explorer)

        # Add buttons to the sidebar
        button_5_video_explorer = QPushButton(f"Video Explorer")
        button_5_video_explorer.clicked.connect(lambda: self.show_window(self.window5.window_index))
        self.sidebar_layout.addWidget(button_5_video_explorer)

        # Add buttons to the sidebar
        button_6_file_shredder = QPushButton(f"Shredder")
        button_6_file_shredder.clicked.connect(lambda: self.show_window(self.window6.window_index))
        self.sidebar_layout.addWidget(button_6_file_shredder)

        # Add buttons to the sidebar
        button_7_visualise = QPushButton(f"Visualise")
        button_7_visualise.clicked.connect(lambda: self.show_window(self.window7.window_index))
        self.sidebar_layout.addWidget(button_7_visualise)

        # Set the default screen to the welcome window
        self.stacked_widget.setCurrentIndex(0)

        self.sidebar.setStyleSheet(styles.sidebar.main_style())

    def show_window(self, window_index: int):
        self.stacked_widget.setCurrentIndex(window_index)

    def apply_system_theme(self, dark_mode):
        if dark_mode:
            self.setStyleSheet(styles.system_theme.dark_style())
        else:  # if light mode
            self.setStyleSheet(styles.system_theme.light_style())

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

    def toggleDarkMode(self):
        self.apply_system_theme(self.dark_mode)
        self.dark_mode = not self.dark_mode
