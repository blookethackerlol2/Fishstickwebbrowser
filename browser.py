from PyQt5.QtWidgets import QTabBar, QTabWidget
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

class CustomWebEngineView(QWebEngineView):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JavaScript error: {message} (line {lineNumber}, source: {sourceID})")

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
        self.new_tab_button.clicked.connect(self.add_new_tab_with_default_url)

        # Style the buttons
        button_style = """
            QPushButton {
                background-color: #007BFF; /* Blue background */
                color: white; /* White text */
                border: none; /* Remove border */
                border-radius: 15px; /* Round shape */
                font-size: 12px; /* Decreased font size */
                width: 30px; /* Width */
                height: 30px; /* Height */
                padding: 0; /* Remove padding to maintain round shape */
            }
            QPushButton:hover {
                background-color: #0056b3; /* Darker blue on hover */
            }
        """

        # Apply style
        for button in [self.back_button, self.forward_button, self.refresh_button, self.home_button, self.new_tab_button]:
            button.setStyleSheet(button_style)
            button.setFixedSize(30, 30)  # Set fixed size to 30x30

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.new_tab_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)  # Add button layout to the top
        main_layout.addWidget(self.url_bar)
        main_layout.addWidget(self.tabs)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Adjust the margins
        main_layout.setContentsMargins(5, 5, 5, 5)  # Set smaller margins for the main layout
        button_layout.setContentsMargins(0, 0, 0, 0)  # No margins for button layout

        self.show()

    def add_new_tab_with_default_url(self):
        """Method to add a new tab with the default URL"""
        self.add_new_tab(QUrl("http://www.google.com"))

    def add_new_tab(self, url):
        webview = CustomWebEngineView()
        webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        tab_index = self.tabs.addTab(webview, "New Tab")
        self.tabs.setCurrentIndex(tab_index)
        webview.setUrl(url)

        # Create a close button for the tab
        close_button = QPushButton("X")
        close_button.setFixedSize(20, 20)  # Set button size
        close_button.setStyleSheet("border-radius: 10px;")  # Make it round
        close_button.clicked.connect(lambda: self.close_tab(tab_index))  # Connect to close function

        # Create a QWidget for the tab button
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        tab_layout.addWidget(QLabel("Tab"))
        tab_layout.addWidget(close_button)

        # Set the tab button to the custom widget
        self.tabs.tabBar().setTabButton(tab_index, QTabBar.RightSide, tab_widget)

    def close_tab(self, index):
        if index >= 0:
            self.tabs.removeTab(index)
            if self.tabs.count() == 0:
                self.add_new_tab_with_default_url()  # Open a new tab with the default URL

    def navigate_home(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  # Add http:// if missing
        current_tab = self.tabs.currentWidget()
        if current_tab:
            try:
                current_tab.setUrl(QUrl(url))
                print(f"Navigating to: {url}")
            except Exception as e:
                print(f"Error navigating to {url}: {e}")

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab and current_tab.history().canGoBack():
            current_tab.history().back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab and current_tab.history().canGoForward():
            current_tab.history().forward()

    def refresh_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())







    
























