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
        self.visited_urls.add(self.url().toString())
        self.update_completer()
        self.check_homepage()

    def check_homepage(self):
        if self.url().toString() == "http://www.google.com/" or self.url().toString() == "https://www.google.com/":
            self.url_bar.clear()
        else:
            self.url_bar.setText(self.url().toString())

    def update_completer(self):
        self.url_bar.completer().model().setStringList(list(self.visited_urls))

    def update_url_bar(self, q):
        if self.url().toString() != "http://www.google.com/" and self.url().toString() != "https://www.google.com/":
            self.url_bar.setText(q.toString())

    def createWindow(self, _type):
        page = CustomWebEngineView(self.url_bar, self.visited_urls)
        self.parent().tabs.addTab(page, "New Tab")
        self.parent().tabs.setCurrentWidget(page)
        return page

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homework Buddy")
        self.resize(800, 600)

        self.visited_urls = set()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Type a URL or search term")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        completer = QCompleter()
        self.url_bar.setCompleter(completer)
        completer.setModel(QStringListModel())

        self.url_bar.setFixedHeight(40)
        self.update_url_bar_width()
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #007BFF;
                border-radius: 20px;
                padding: 10px;
            }
        """)

        self.add_new_tab(QUrl("http://www.google.com"))

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

        button_style = """
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 12px;
                width: 30px;
                height: 30px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

        for button in [self.back_button, self.forward_button, self.refresh_button, self.home_button, self.new_tab_button]:
            button.setStyleSheet(button_style)
            button.setFixedSize(30, 30)

        button_layout = QHBoxLayout()
        for button in [self.back_button, self.forward_button, self.refresh_button, self.home_button, self.new_tab_button]:
            button_layout.addWidget(button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.url_bar, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.version_label = QLabel("V0.5 (alpha)" ("Any bugs? contact kkaow9393@gmail.com"))
        self.version_label.setStyleSheet("color: gray; font-size: 10px;")
        self.version_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.statusBar().addPermanentWidget(self.version_label)

        self.show()

    def update_url_bar_width(self):
        width = int(self.width() * 0.85)
        self.url_bar.setFixedWidth(width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_url_bar_width()

    def add_new_tab_with_default_url(self):
        self.add_new_tab(QUrl("http://www.google.com"))

    def add_new_tab(self, url):
        webview = CustomWebEngineView(self.url_bar, self.visited_urls)
        webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        tab_index = self.tabs.addTab(webview, "New Tab")
        self.tabs.setCurrentIndex(tab_index)
        webview.setUrl(url)

        close_button = QPushButton("X")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #31312B;
            }
        """)
        close_button.clicked.connect(lambda: self.close_tab(tab_index))

        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(QLabel("Tab"))
        tab_layout.addWidget(close_button)

        self.tabs.tabBar().setTabButton(tab_index, QTabBar.RightSide, tab_widget)

    def close_tab(self, index):
        if index >= 0:
            self.tabs.removeTab(index)
            if self.tabs.count() == 0:
                self.add_new_tab_with_default_url()

    def navigate_home(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        input_text = self.url_bar.text().strip()
        if input_text:
            if not input_text.startswith(('http://', 'https://')):
                input_text = "https://" + input_text

            current_tab = self.tabs.currentWidget()
            if current_tab:
                try:
                    current_tab.setUrl(QUrl(input_text))
                    self.visited_urls.add(input_text)
                    self.update_completer()
                except Exception as e:
                    print(f"Error navigating to URL: {e}")

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
