from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, \
    QAction
from python.primary_windows.organise_window import OrganiseWindow
from python.primary_windows.optimise_window import OptimiseWindow
from python.primary_windows.visualise_window import VisualiseWindow
from python.primary_windows.file_sharing_window import FileUploader
from python.primary_windows.search_window import SearchWindow
import styles.system_theme
import styles.sidebar   # Import the sidebar style module
from requests import Session    # Import the requests module

# Import the FileSystemNodeModel class from the model modules
class MainWindow(QMainWindow):
    """
    Main window for the application. This is the window that the user sees after the splash window.
    """
    def __init__(self, fileSystemModel):
        super().__init__()
        self.fileSystemModel = fileSystemModel
        self.session = Session()  # Initialize a Session object here

        web_engine_profile = QWebEngineProfile.defaultProfile()
        web_engine_profile.setHttpUserAgent('CustomUserAgentString PyQt')

        # Use this profile in your QWebEngineView
        web_view = QWebEngineView()
        web_view.setPage(QWebEnginePage(web_engine_profile))

        self.loggedIn = False  # Initialize login status

        # Set the main window's title and initial size
        self.setWindowTitle("K.L.A.A.S. - Knowledge Lookup and Archive Access Service")
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
        self.search_window = SearchWindow(0, self.fileSystemModel)
        self.organise_window = OrganiseWindow(1, self.fileSystemModel)
        self.optimise_window = OptimiseWindow(2, self.fileSystemModel)
        self.visualise_window = VisualiseWindow(3, self.fileSystemModel)
        self.file_sharing_window = FileUploader(4, self.fileSystemModel)

        # Add the sidebar to the main layout
        self.main_layout.addWidget(self.sidebar, 2)  # 2/10 of the space for the sidebar

        # Create a stacked widget to hold the different screens
        self.stacked_widget = QStackedWidget()

        # Add windows to the stacked widget
        self.stacked_widget.addWidget(self.search_window) # Add the welcome window
        self.stacked_widget.addWidget(self.organise_window) # Add the file explorer window
        self.stacked_widget.addWidget(self.optimise_window) # Add the music explorer window
        self.stacked_widget.addWidget(self.visualise_window) # Add the visualise window
        self.stacked_widget.addWidget(self.file_sharing_window) # Add the file uploader window
        # Add the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget, 8)  # Adjusting space for main content

        # Now, set the FileSystemNodeModel instance to the visualise window
        self.visualise_window.setFileSystemModel(self.fileSystemModel)


        # Add the stacked widget to the main layout
        self.file_sharing_window.uploadFinished.connect(self.showWebView)

        # Add buttons to the sidebar
        button_0_file_search = QPushButton(f"Search")
        icon = QIcon("ui/images/icons/search_icon.svg")  # Replace with the path to your SVG icon
        button_0_file_search.setIcon(icon)
        button_0_file_search.setIconSize(QSize(24, 24))  # Adjust the size as needed
        button_0_file_search.clicked.connect(lambda: self.show_window(self.search_window.window_index))
        self.sidebar_layout.addWidget(button_0_file_search)

        # Add buttons to the sidebar
        button_1_organise = QPushButton(f"Organise")
        icon = QIcon("ui/images/icons/organise_icon.png")  # Replace with the path to your SVG icon
        button_1_organise.setIcon(icon)
        button_1_organise.setIconSize(QSize(24, 24))  # Adjust the size as needed
        button_1_organise.clicked.connect(lambda: self.show_window(self.organise_window.window_index))
        self.sidebar_layout.addWidget(button_1_organise)

        # Add buttons to the sidebar
        button_2_optimise = QPushButton(f"Optimise")
        icon = QIcon("ui/images/icons/optimise_icon.png")  # Replace with the path to your SVG icon
        button_2_optimise.setIcon(icon)
        button_2_optimise.setIconSize(QSize(24, 24))  # Adjust the size as needed
        button_2_optimise.clicked.connect(lambda: self.show_window(self.optimise_window.window_index))
        self.sidebar_layout.addWidget(button_2_optimise)

        # Add buttons to the sidebar
        button_3_visualise = QPushButton(f"Visualise")
        icon = QIcon("ui/images/icons/visualise_icon.png")  # Replace with the path to your SVG icon
        button_3_visualise.setIcon(icon)
        button_3_visualise.setIconSize(QSize(24, 24))  # Adjust the size as needed
        button_3_visualise.clicked.connect(lambda: self.show_window(self.visualise_window.window_index))
        self.sidebar_layout.addWidget(button_3_visualise)

        # Add buttons to the sidebar
        button_4_file_sharing = QPushButton(f"File Sharing")
        icon = QIcon("ui/images/icons/cloud_icon.svg")  # Replace with the path to your SVG icon
        button_4_file_sharing.setIcon(icon)
        button_4_file_sharing.setIconSize(QSize(24, 24))  # Adjust the size as needed
        button_4_file_sharing.clicked.connect(self.checkLoginAndShow)
        self.sidebar_layout.addWidget(button_4_file_sharing)

        # Set the default screen to the welcome window
        self.stacked_widget.setCurrentIndex(0)

        self.sidebar.setStyleSheet(styles.sidebar.main_style())

    def show_window(self, window_index: int):
        """
        Show the window at the given index in the stacked widget.
        """
        self.stacked_widget.setCurrentIndex(window_index)

    def showWebView(self, url):
        """
        Show a web view with the given URL.
        """
        # Check if the last widget is already a QWebEngineView to avoid duplicates
        if isinstance(self.stacked_widget.currentWidget(), QWebEngineView):
            # Update the URL of the existing web view
            self.stacked_widget.currentWidget().setUrl(QUrl(url))
        else:
            # Create a new web view and add it to the stack
            webView = QWebEngineView()
            webView.setUrl(QUrl(url))
            self.stacked_widget.addWidget(webView)
            self.stacked_widget.setCurrentWidget(webView)

    def setupWebView(self, webView):
        """
        Connect the URL changed signal of the QWebEngineView to a slot.
        """
        webView.urlChanged.connect(self.onWebViewUrlChanged)

    def onWebViewUrlChanged(self, url):
        print("URL changed to:", url.toString())  # Add this line for debugging
            # self.show_window(self.file_sharing_window.window_index)

    def apply_system_theme(self, dark_mode):
        if dark_mode:
            self.setStyleSheet(styles.system_theme.dark_style())
        else:  # if light mode
            self.setStyleSheet(styles.system_theme.light_style())

    def createMenuBar(self):
        """
        Create the menu bar for the main window.
        """
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

    def checkLoginAndShow(self):
        if self.isUserLoggedIn():
            self.show_window(
                self.file_sharing_window.window_index)  # This is the correct index for your file sharing window
        else:
            self.showLoginWebView()

    def isUserLoggedIn(self):
        """
        Check if the user is logged in.
        """
        return self.loggedIn

    def showLoginWebView(self):
        """
        Show a web view with the login page.
        """
        loginUrl = "http://127.0.0.1:5000/login?view=pyqt"  # URL of your HTML login page

        # Find an existing QWebEngineView or create a new one
        webView = None
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, QWebEngineView):
                webView = widget
                break

        if webView is None:
            webView = QWebEngineView()
            webView.urlChanged.connect(self.onWebViewUrlChanged)  # Ensure this is connected
            self.stacked_widget.addWidget(webView)

        # Set the URL to the login page
        webView.setUrl(QUrl(loginUrl))

        # Make sure the QWebEngineView is visible
        self.stacked_widget.setCurrentWidget(webView)