# login_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from database import session, User, UserRole

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 280, 150)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel('Username')
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password')
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            QMessageBox.information(self, 'Login', f'Welcome {user.username}!')
            self.open_role_window(user)
        else:
            QMessageBox.warning(self, 'Login', 'Invalid credentials')

    def open_role_window(self, user):
        if user.role == UserRole.ADMIN:
            from admin_window import AdminWindow
            self.admin_window = AdminWindow(user)
            self.admin_window.show()
        elif user.role == UserRole.WAITER:
            from waiter_window import WaiterWindow
            self.waiter_window = WaiterWindow(user)
            self.waiter_window.show()
        elif user.role == UserRole.CHEF:
            from chef_window import ChefWindow
            self.chef_window = ChefWindow(user)
            self.chef_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
