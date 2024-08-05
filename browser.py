from PyQt5.QtWidgets import QTabBar, QTabWidget
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QDateTime
from PyQt5.QtWebEngineCore import QWebEngineCookieStore
from PyQt5.QtNetwork import QNetworkCookie  # Corrected import

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tabbed Browser")
        self.resize(800, 600)  # Set initial size of the window

        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Type a URL (including http or https)")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Initialize first tab
        self.add_new_tab(QUrl("http://www.google.com"))

        # Navigation buttons
        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.go_forward)

        self.refresh_button = QPushButton("R")
        self.refresh_button.clicked.connect(self.refresh_current_tab)

        self.home_button = QPushButton("H")
        self.home_button.clicked.connect(self.navigate_home)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_new_tab_with_de)






    
























