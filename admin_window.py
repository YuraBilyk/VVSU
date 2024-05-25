# admin_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton, QMessageBox
from database import session, User

class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Admin Panel')
        self.setGeometry(100, 100, 600, 400)
        self.user = user
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.user_list = QListWidget()
        self.load_users()
        layout.addWidget(self.user_list)

        self.add_user_button = QPushButton('Add User')
        self.add_user_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_button)

        self.fire_user_button = QPushButton('Fire User')
        self.fire_user_button.clicked.connect(self.fire_user)
        layout.addWidget(self.fire_user_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_users(self):
        self.user_list.clear()
        users = session.query(User).all()
        for user in users:
            self.user_list.addItem(f"{user.id} - {user.username} ({user.role}) - {user.status}")

    def add_user(self):
        from add_user_window import AddUserWindow
        self.add_user_window = AddUserWindow(self)
        self.add_user_window.show()

    def fire_user(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            user_id = int(selected_user.text().split(' ')[0])
            user = session.query(User).get(user_id)
            user.status = 'fired'
            session.commit()
            self.load_users()
            QMessageBox.information(self, 'User Fired', f'{user.username} has been fired.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_window = AdminWindow(None)
    admin_window.show()
    sys.exit(app.exec_())
