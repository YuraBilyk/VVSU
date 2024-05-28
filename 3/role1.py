# role1.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from database import session, Task, TaskStatus

class Role1Window(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Панель Роль 1')
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

        # Кнопки для управления задачами
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

    def start_task(self):
        # Начало выполнения задачи
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = int(self.task_table.item(selected_row, 0).text())
            task = session.query(Task).get(task_id)
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.IN_PROGRESS
                task.user1_id = self.user.id  # Назначение задачи пользователю
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
    window = Role1Window(None)
    window.show()
    app.exec_()
