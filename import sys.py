import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QTabBar, QLabel, QCompleter
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt, QStringListModel

class CustomWebEngineView(QWebEngineView):
    def __init__(self, url_bar, visited_urls):
        super().__init__()
        self.url_bar = url_bar
        self.visited_urls = visited_urls
        self.loadFinished.connect(self.on_load_finished)
        self.urlChanged.connect(self.update_url_bar)

    def on_load_finished(self, result):
        self.visited_urls.add(self.url().toString())  # Add the current URL to visited URLs
        self.update_completer()
        self.check_homepage()

    def check_homepage(self):
        # Hide the URL bar text if on the Google homepage
        if self.url().toString() == "http://www.google.com/" or self.url().toString() == "https://www.google.com/":
            self.url_bar.clear()
        else:
            self.url_bar.setText(self.url().toString())

    def update_completer(self):
        # Update the completer with the current visited URLs
        self.url_bar.completer().model().setStringList(list(self.visited_urls))

    def update_url_bar(self, q):
        if self.url().toString() != "http://www.google.com/" and self.url().toString() != "https://www.google.com/":
            self.url_bar.setText(q.toString())

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homework Buddy")
        self.resize(800, 600)

        # Store visited URLs
        self.visited_urls = set()

        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Type a URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Create a QCompleter for the URL bar
        completer = QCompleter()
        self.url_bar.setCompleter(completer)
        completer.setModel(QStringListModel())  # Initialize with an empty model

        # Set URL bar style
        self.url_bar.setFixedHeight(40)  # Set fixed height for shorter URL bar (20% shorter)
        self.update_url_bar_width()  # Set initial width
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #007BFF;  /* Blue border */
                border-radius: 20px;        /* Rounded corners */
                padding: 10px;               /* Padding for better appearance */
            }
        """)

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
        for button in [self.back_button, self.forward_button, self.refresh_button, self.home_button, self.new_tab_button]:
            button_layout.addWidget(button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)

        # Center the URL bar
        main_layout.addWidget(self.url_bar, alignment=Qt.AlignHCenter)  # Center the URL bar
        main_layout.addWidget(self.tabs)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.show()

    def update_url_bar_width(self):
        """Update the URL bar width to be 85% of the main window width."""
        width = int(self.width() * 0.85)  # Set to 85% width
        self.url_bar.setFixedWidth(width)  # Set the width of the URL bar

    def resizeEvent(self, event):
        """Override the resize event to update URL bar width."""
        super().resizeEvent(event)
        self.update_url_bar_width()

    def add_new_tab_with_default_url(self):
        self.add_new_tab(QUrl("http://www.google.com"))

    def add_new_tab(self, url):
        webview = CustomWebEngineView(self.url_bar, self.visited_urls)  # Pass the URL bar and visited URLs to the webview
        webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        tab_index = self.tabs.addTab(webview, "New Tab")
        self.tabs.setCurrentIndex(tab_index)
        webview.setUrl(url)

        # Create a close button for the tab
        close_button = QPushButton("X")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #000000; /* Black Background */
                color: white; /* White text */
                border: none; /* Remove border */
                border-radius: 10px; /* Round shape */
                font-size: 12px; /* Font size */
            }
            QPushButton:hover {
                background-color: #31312B; /* Dark grey on hover */
            }
        """)
        close_button.clicked.connect(lambda: self.close_tab(tab_index))

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
        input_text = self.url_bar.text().strip()  # Get the text and strip any extra whitespace
        if input_text:
            # If the input doesn't start with 'http://' or 'https://', prepend 'https://'
            if not input_text.startswith(('http://', 'https://')):
                input_text = "https://" + input_text  # Default to https://

            current_tab = self.tabs.currentWidget()
            if current_tab:
                try:
                    current_tab.setUrl(QUrl(input_text))  # Navigate to the input as a URL
                    self.visited_urls.add(input_text)  # Add to visited URLs
                    self.update_completer()  # Update the completer
                except Exception as e:
                    print(f"Error navigating to URL: {e}")  # Print error message for debugging

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())






