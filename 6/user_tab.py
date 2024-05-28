# user_tab.py
# Этот файл отвечает за вкладку управления пользователями.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QInputDialog, QLineEdit
from database import session, User, UserRole

class UserTab(QWidget):  # Ранее 'EmployeeTab'
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(['ID', 'Username', 'Role', 'Status'])  # Ранее 'Имя пользователя', 'Роль', 'Статус'
        self.user_table.setSortingEnabled(True)
        self.load_users()
        layout.addWidget(self.user_table)

        self.add_user_button = QPushButton('Add User')  # Ранее 'Добавить пользователя'
        self.add_user_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_button)

        self.deactivate_user_button = QPushButton('Deactivate User')  # Ранее 'Уволить пользователя'
        self.deactivate_user_button.clicked.connect(self.deactivate_user)
        layout.addWidget(self.deactivate_user_button)

        self.setLayout(layout)

    def load_users(self):
        self.user_table.setRowCount(0)
        users = session.query(User).all()
        for user in users:
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            self.user_table.setItem(row_position, 0, QTableWidgetItem(str(user.id)))
            self.user_table.setItem(row_position, 1, QTableWidgetItem(user.username))
            self.user_table.setItem(row_position, 2, QTableWidgetItem(user.role.value))
            self.user_table.setItem(row_position, 3, QTableWidgetItem(user.status))

    def add_user(self):
        username, ok = QInputDialog.getText(self, 'Add User', 'Enter username:')  # Ранее 'Добавить пользователя', 'Введите имя пользователя:'
        if ok and username:
            password, ok = QInputDialog.getText(self, 'Add User', 'Enter password:', QLineEdit.Password)  # Ранее 'Введите пароль:'
            if ok and password:
                role, ok = QInputDialog.getItem(self, 'Add User', 'Select role:', [role.value for role in UserRole], 0, False)  # Ранее 'Выберите роль:'
                if ok and role:
                    user = User(username=username, password=password, role=UserRole(role))
                    session.add(user)
                    session.commit()
                    self.load_users()
                    QMessageBox.information(self, 'Success', 'User added successfully.')  # Ранее 'Пользователь успешно добавлен'

    def deactivate_user(self):
        selected_row = self.user_table.currentRow()
        if selected_row >= 0:
            user_id = int(self.user_table.item(selected_row, 0).text())
            user = session.query(User).get(user_id)
            user.status = 'inactive'  # Ранее 'уволен'
            session.commit()
            self.load_users()
            QMessageBox.information(self, 'User Deactivated', f'{user.username} has been deactivated.')  # Ранее '{user.username} уволен'
