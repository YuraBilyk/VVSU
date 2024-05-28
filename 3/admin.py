# admin.py
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox, QLineEdit
from database import session, User, UserRole, Task, Shift

class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Панель Администратора')
        self.setGeometry(200, 200, 800, 600)
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        # Создание вкладок для различных функций администратора
        self.tabs = QTabWidget()
        
        self.user_tab = QWidget()
        self.task_tab = QWidget()
        self.shift_tab = QWidget()
        
        self.tabs.addTab(self.user_tab, "Пользователи")
        self.tabs.addTab(self.task_tab, "Задачи")
        self.tabs.addTab(self.shift_tab, "Смены")
        
        self.setup_user_tab()
        self.setup_task_tab()
        self.setup_shift_tab()
        
        self.setCentralWidget(self.tabs)
    
    def setup_user_tab(self):
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(['ID', 'Имя пользователя', 'Роль', 'Статус'])
        self.user_table.setSortingEnabled(True)
        layout.addWidget(self.user_table)
        self.load_users()

        button_layout = QHBoxLayout()

        self.add_user_button = QPushButton('Добавить пользователя')
        self.add_user_button.clicked.connect(self.add_user)
        button_layout.addWidget(self.add_user_button)
        
        self.fire_user_button = QPushButton('Уволить пользователя')
        self.fire_user_button.clicked.connect(self.fire_user)
        button_layout.addWidget(self.fire_user_button)

        layout.addLayout(button_layout)

        self.user_tab.setLayout(layout)
    
    def setup_task_tab(self):
        layout = QVBoxLayout()
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(['ID задачи', 'Название задачи', 'Описание задачи', 'Статус', 'Исполнитель'])
        self.task_table.setSortingEnabled(True)
        layout.addWidget(self.task_table)
        self.load_tasks()
        
        self.task_tab.setLayout(layout)
    
    def setup_shift_tab(self):
        layout = QVBoxLayout()
        self.shift_table = QTableWidget()
        self.shift_table.setColumnCount(4)
        self.shift_table.setHorizontalHeaderLabels(['ID смены', 'Название', 'Время', 'Пользователи'])
        self.shift_table.setSortingEnabled(True)
        layout.addWidget(self.shift_table)
        self.load_shifts()

        button_layout = QHBoxLayout()

        self.add_shift_button = QPushButton('Добавить смену')
        self.add_shift_button.clicked.connect(self.add_shift)
        button_layout.addWidget(self.add_shift_button)
        
        self.assign_user_button = QPushButton('Назначить пользователя на смену')
        self.assign_user_button.clicked.connect(self.assign_user)
        button_layout.addWidget(self.assign_user_button)

        layout.addLayout(button_layout)
        
        self.shift_tab.setLayout(layout)

    def load_users(self):
        # Загрузка и отображение пользователей из базы данных
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
        # Добавление нового пользователя
        username, ok = QInputDialog.getText(self, 'Добавить пользователя', 'Введите имя пользователя:')
        if ok and username:
            password, ok = QInputDialog.getText(self, 'Добавить пользователя', 'Введите пароль:', QLineEdit.Password)
            if ok and password:
                role, ok = QInputDialog.getItem(self, 'Добавить пользователя', 'Выберите роль:', [role.value for role in UserRole], 0, False)
                if ok and role:
                    user = User(username=username, password=password, role=UserRole(role))
                    session.add(user)
                    session.commit()
                    self.load_users()
                    QMessageBox.information(self, 'Успех', 'Пользователь успешно добавлен')

    def fire_user(self):
        # Увольнение пользователя
        selected_row = self.user_table.currentRow()
        if selected_row >= 0:
            user_id = int(self.user_table.item(selected_row, 0).text())
            user = session.query(User).get(user_id)
            user.status = 'уволен'
            session.commit()
            self.load_users()
            QMessageBox.information(self, 'Успех', f'Пользователь {user.username} уволен.')

    def load_tasks(self):
        # Загрузка и отображение задач из базы данных
        self.task_table.setRowCount(0)
        tasks = session.query(Task).all()
        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(str(task.id)))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(task.title))
            self.task_table.setItem(row_position, 2, QTableWidgetItem(task.description))
            self.task_table.setItem(row_position, 3, QTableWidgetItem(task.status.value))
            executor = task.user1.username if task.user1 else 'Нет'
            self.task_table.setItem(row_position, 4, QTableWidgetItem(executor))

    def load_shifts(self):
        # Загрузка и отображение смен из базы данных
        self.shift_table.setRowCount(0)
        shifts = session.query(Shift).all()
        for shift in shifts:
            row_position = self.shift_table.rowCount()
            self.shift_table.insertRow(row_position)
            self.shift_table.setItem(row_position, 0, QTableWidgetItem(str(shift.id)))
            self.shift_table.setItem(row_position, 1, QTableWidgetItem(shift.name))
            self.shift_table.setItem(row_position, 2, QTableWidgetItem(shift.time))
            users = ', '.join([user.username for user in shift.users])
            self.shift_table.setItem(row_position, 3, QTableWidgetItem(users))

    def add_shift(self):
        # Добавление новой смены
        shift_name, ok = QInputDialog.getText(self, 'Добавить смену', 'Введите название смены:')
        if ok and shift_name:
            shift_time, ok = QInputDialog.getText(self, 'Добавить смену', 'Введите время смены (например, 09:00 - 17:00):')
            if ok and shift_time:
                shift = Shift(name=shift_name, time=shift_time)
                session.add(shift)
                session.commit()
                self.load_shifts()
                QMessageBox.information(self, 'Успех', 'Смена успешно добавлена')

    def assign_user(self):
        # Назначение пользователя на смену
        selected_row = self.shift_table.currentRow()
        if selected_row >= 0:
            shift_id = int(self.shift_table.item(selected_row, 0).text())
            shift = session.query(Shift).get(shift_id)
            users = session.query(User).filter(User.role.in_([UserRole.ROLE1, UserRole.ROLE2])).all()
            user_list = [user.username for user in users]
            user_name, ok = QInputDialog.getItem(self, 'Назначить пользователя', 'Выберите пользователя:', user_list, 0, False)
            if ok and user_name:
                user = session.query(User).filter_by(username=user_name).first()
                if user:
                    shift.users.append(user)
                    session.commit()
                    self.load_shifts()
                    QMessageBox.information(self, 'Успех', f'{user.username} назначен на смену {shift.name}')

if __name__ == '__main__':
    app = QApplication([])
    window = AdminWindow(None)
    window.show()
    app.exec_()
