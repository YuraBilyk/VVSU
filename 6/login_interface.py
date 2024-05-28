# login_interface.py
# Этот файл отвечает за окно входа в систему.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from database import session, User, UserRole

class LoginInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(200, 400, 380, 250)
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
            if user.status == 'inactive':  # Ранее 'уволен'
                QMessageBox.warning(self, 'Login', 'Your account is deactivated.')
            else:
                QMessageBox.information(self, 'Login', f'Welcome, {user.username}!')
                self.open_role_window(user)
        else:
            QMessageBox.warning(self, 'Login', 'Invalid credentials.')

    def open_role_window(self, user):
        if user.role == UserRole.MANAGER:  # Ранее 'admin'
            from admin_window import ManagerInterface  # Ранее 'admin_window'
            self.admin_window = ManagerInterface(user)
            self.admin_window.show()
        elif user.role == UserRole.ASSOCIATE:  # Ранее 'waiter'
            from associate_interface import AssociateInterface  # Ранее 'waiter_window'
            self.associate_interface = AssociateInterface(user)
            self.associate_interface.show()
        elif user.role == UserRole.SPECIALIST:  # Ранее 'chef'
            from specialist_interface import SpecialistInterface  # Ранее 'chef_window'
            self.specialist_interface = SpecialistInterface(user)
            self.specialist_interface.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_interface = LoginInterface()
    login_interface.show()
    sys.exit(app.exec_())
