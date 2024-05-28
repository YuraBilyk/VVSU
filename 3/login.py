# login.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from database import session, User, UserRole

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход в систему')
        self.setGeometry(200, 200, 400, 150)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.username_label = QLabel('Имя пользователя')
        left_layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        right_layout.addWidget(self.username_input)

        self.password_label = QLabel('Пароль')
        left_layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        right_layout.addWidget(self.password_input)

        form_layout.addLayout(left_layout)
        form_layout.addLayout(right_layout)

        main_layout.addLayout(form_layout)

        self.login_button = QPushButton('Войти')
        main_layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.check_login)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def check_login(self):
        # Проверка учетных данных пользователя
        username = self.username_input.text()
        password = self.password_input.text()
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            if user.status == 'уволен':
                QMessageBox.warning(self, 'Ошибка', 'Ваш аккаунт деактивирован.')
            else:
                self.open_role_window(user)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверные учетные данные')

    def open_role_window(self, user):
        # Открытие окна в зависимости от роли пользователя
        if user.role == UserRole.ADMIN:
            from admin import AdminWindow
            self.admin_window = AdminWindow(user)
            self.admin_window.show()
        elif user.role == UserRole.ROLE1:
            from role1 import Role1Window  # Замените 'role1' на соответствующую роль, например, 'mechanic'
            self.role1_window = Role1Window(user)
            self.role1_window.show()
        elif user.role == UserRole.ROLE2:
            from role2 import Role2Window  # Замените 'role2' на соответствующую роль, например, 'diagnostician'
            self.role2_window = Role2Window(user)
            self.role2_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
