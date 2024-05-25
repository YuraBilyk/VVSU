# add_user_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QComboBox
from database import session, User, UserRole

class AddUserWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add User')
        self.setGeometry(100, 100, 300, 200)
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

        self.role_label = QLabel('Role')
        layout.addWidget(self.role_label)
        self.role_input = QComboBox()
        self.role_input.addItems([role.value for role in UserRole])
        layout.addWidget(self.role_input)

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        if username and password and role:
            user = User(username=username, password=password, role=UserRole(role))
            session.add(user)
            session.commit()
            self.parent().load_users()
            QMessageBox.information(self, 'Success', 'User added successfully')
            self.close()
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields are required')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_user_window = AddUserWindow()
    add_user_window.show()
    sys.exit(app.exec_())
