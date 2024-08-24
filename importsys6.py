import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, 
                             QTabWidget, QTabBar, QLabel, QCompleter, QDialog, QFormLayout, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt, QStringListModel

# Dummy password strength API URL for illustration
PASSWORD_STRENGTH_API_URL = "https://api.passwordstrength.com/estimate"  # Replace with an actual API if available

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

class CustomTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
        else:
            QMessageBox.warning(self, "Cannot Close Tab", "At least one tab must be open.")

class LoginPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)

        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.handle_signup)

        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        self.setLayout(layout)

    def handle_login(self):
        # Simulated login logic
        username = self.username.text().strip()
        password = self.password.text().strip()
        if username and password:
            # Replace with actual authentication logic
            print("Logging in with username:", username)
            self.accept()  # Close dialog and proceed
        else:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")

    def handle_signup(self):
        signup_dialog = SignupPage(self)
        if signup_dialog.exec_() == QDialog.Accepted:
            print("Sign up successful")
        else:
            print("Sign up cancelled")

class SignupPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.setFixedSize(300, 250)

        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setEnabled(False)  # Initially disabled
        self.signup_button.clicked.connect(self.handle_signup)

        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        layout.addWidget(self.signup_button)
        self.setLayout(layout)

        self.password.textChanged.connect(self.validate_password)

    def validate_password(self):
        password = self.password.text().strip()
        if len(password) < 8:
            self.signup_button.setEnabled(False)
            return

        # Simulated password strength check
        estimated_crack_time = "1 min"  # Placeholder value

        if self.is_secure_password(estimated_crack_time):
            self.signup_button.setEnabled(True)
        else:
            self.signup_button.setEnabled(False)

    def is_secure_password(self, crack_time):
        crack_time_minutes = int(crack_time.split()[0])
        return crack_time_minutes >= 10

    def handle_signup(self):
        QMessageBox.warning(self, "Sign Up Disabled", "Sign-up functionality is currently disabled.")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homework Buddy")
        self.resize(800, 600)

        self.visited_urls = set()
        self.tabs = CustomTabWidget()  # Use CustomTabWidget
        self.setCentralWidget(self.tabs)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Type a URL")
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

        self.version_label = QLabel("V0.5 (alpha) - Any bugs? contact kkaow9393@gmail.com")
        self.version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.version_label)

        self.show_login_dialog()

    def update_url_bar_width(self):
        self.url_bar.setFixedWidth(int(self.width() * 0.8))  # Ensure width is an integer

    def show_login_dialog(self):
        self.login_page = LoginPage(self)
        if self.login_page.exec_() == QDialog.Accepted:
            self.init_browser()
        else:
            self.close()  # Close application if login is cancelled

    def init_browser(self):
        self.add_new_tab(QUrl("http://www.google.com"))

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl("http://www.google.com")
        new_tab = CustomWebEngineView(self.url_bar, self.visited_urls)
        new_tab.setUrl(qurl)
        new_tab.setPage(new_tab.page())
        self.tabs.addTab(new_tab, "New Tab")

    def add_new_tab_with_default_url(self):
        self.add_new_tab()

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def go_back(self):
        self.tabs.currentWidget().back()

    def go_forward(self):
        self.tabs.currentWidget().forward()

    def refresh_current_tab(self):
        self.tabs.currentWidget().reload()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com/"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
