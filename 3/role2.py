# role2.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLineEdit, QLabel, QDialog
from PyQt5.QtCore import pyqtSignal
from database import session, Task, TaskStatus, User

class CreateTaskDialog(QDialog):
    task_created = pyqtSignal()

    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle('Создать задачу')
        self.user_id = user_id
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Поля ввода для названия, описания задачи и количества гостей
        self.title_label = QLabel('Название задачи')
        left_layout.addWidget(self.title_label)
        self.title_input = QLineEdit()
        right_layout.addWidget(self.title_input)

        self.description_label = QLabel('Описание задачи')
        left_layout.addWidget(self.description_label)
        self.description_input = QLineEdit()
        right_layout.addWidget(self.description_input)

        self.guest_count_label = QLabel('Количество гостей')
        left_layout.addWidget(self.guest_count_label)
        self.guest_count_input = QLineEdit()
        right_layout.addWidget(self.guest_count_input)

        form_layout.addLayout(left_layout)
        form_layout.addLayout(right_layout)
        layout.addLayout(form_layout)

        self.create_task_button = QPushButton('Создать задачу')
        self.create_task_button.clicked.connect(self.create_task)
        layout.addWidget(self.create_task_button)

        self.setLayout(layout)

    def create_task(self):
        # Создание новой задачи
        title = self.title_input.text()
        description = self.description_input.text()
        guest_count = self.guest_count_input.text()

        if title and description and guest_count:
            task = Task(
                title=title,
                description=f'{description}, Количество гостей: {guest_count}',
                user2_id=self.user_id,
                status=TaskStatus.PENDING
            )
            session.add(task)
            session.commit()
            self.task_created.emit()
            QMessageBox.information(self, 'Задача создана', 'Новая задача успешно создана.')
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка ввода', 'Все поля обязательны для заполнения.')

class Role2Window(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Панель Роль 2')
        self.setGeometry(200, 200, 600, 400)
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Таблица для отображения задач
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(['ID задачи', 'Название задачи', 'Описание задачи', 'Статус', 'Исполнитель'])
        self.task_table.setSortingEnabled(True)
        layout.addWidget(self.task_table)
        self.load_tasks()

        button_layout = QHBoxLayout()

        # Кнопки для создания, начала и завершения задач
        self.create_task_button = QPushButton('Создать задачу')
        self.create_task_button.clicked.connect(self.open_create_task_dialog)
        button_layout.addWidget(self.create_task_button)

        self.start_task_button = QPushButton('Начать задачу')
        self.start_task_button.clicked.connect(self.start_task)
        button_layout.addWidget(self.start_task_button)

        self.complete_task_button = QPushButton('Завершить задачу')
        self.complete_task_button.clicked.connect(self.complete_task)
        button_layout.addWidget(self.complete_task_button)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_tasks(self):
        # Загрузка и отображение задач из базы данных
        self.task_table.setRowCount(0)
        tasks = session.query(Task).filter_by(user2_id=self.user.id).all()
        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(str(task.id)))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(task.title))
            self.task_table.setItem(row_position, 2, QTableWidgetItem(task.description))
            self.task_table.setItem(row_position, 3, QTableWidgetItem(task.status.value))
            executor = task.user2.username if task.user2 else 'Нет'
            self.task_table.setItem(row_position, 4, QTableWidgetItem(executor))

    def open_create_task_dialog(self):
        # Открытие диалога для создания новой задачи
        self.create_task_dialog = CreateTaskDialog(self.user.id)
        self.create_task_dialog.task_created.connect(self.load_tasks)
        self.create_task_dialog.exec_()

    def start_task(self):
        # Начало выполнения задачи
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = int(self.task_table.item(selected_row, 0).text())
            task = session.query(Task).get(task_id)
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.IN_PROGRESS
                session.commit()
                self.load_tasks()
                QMessageBox.information(self, 'Задача начата', f'Задача {task.id} начата.')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Можно начать только ожидающие задачи.')

    def complete_task(self):
        # Завершение выполнения задачи
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = int(self.task_table.item(selected_row, 0).text())
            task = session.query(Task).get(task_id)
            if task.status == TaskStatus.IN_PROGRESS:
                task.status = TaskStatus.COMPLETED
                session.commit()
                self.load_tasks()
                QMessageBox.information(self, 'Задача завершена', f'Задача {task.id} завершена.')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Можно завершить только задачи в процессе выполнения.')

if __name__ == '__main__':
    app = QApplication([])
    window = Role2Window(None)
    window.show()
    app.exec_()
