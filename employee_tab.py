# employee_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QInputDialog, QLineEdit
from database import session, User, UserRole

class EmployeeTab(QWidget):
    def __init__(self):
        super().__init__()
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

        self.setLayout(layout)

    def load_users(self):
        self.user_list.clear()
        users = session.query(User).all()
        for user in users:
            self.user_list.addItem(f"{user.id} - {user.username} ({user.role}) - {user.status}")

    def add_user(self):
        username, ok = QInputDialog.getText(self, 'Add User', 'Enter username:')
        if ok and username:
            password, ok = QInputDialog.getText(self, 'Add User', 'Enter password:', QLineEdit.Password)
            if ok and password:
                role, ok = QInputDialog.getItem(self, 'Add User', 'Select role:', [role.value for role in UserRole], 0, False)
                if ok and role:
                    user = User(username=username, password=password, role=UserRole(role))
                    session.add(user)
                    session.commit()
                    self.load_users()
                    QMessageBox.information(self, 'Success', 'User added successfully')

    def fire_user(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            user_id = int(selected_user.text().split(' ')[0])
            user = session.query(User).get(user_id)
            user.status = 'fired'
            session.commit()
            self.load_users()
            QMessageBox.information(self, 'User Fired', f'{user.username} has been fired.')
