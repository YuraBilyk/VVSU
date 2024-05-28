# add_task_window.py
# Этот файл отвечает за окно добавления задачи (ранее заказ).

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from database import session, Task, TaskStatus, User

class AddTaskWindow(QMainWindow):  # Ранее 'AddOrderWindow'
    task_added = pyqtSignal()  # Ранее 'order_added'

    def __init__(self, associate):  # Ранее 'waiter'
        super().__init__()
        self.setWindowTitle('Add Task')  # Ранее 'Добавить заказ'
        self.setGeometry(100, 100, 300, 200)
        self.associate = associate  # Ранее 'waiter'
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.reference_label = QLabel('Reference Number')  # Ранее 'Номер стола'
        layout.addWidget(self.reference_label)
        self.reference_input = QLineEdit()
        layout.addWidget(self.reference_input)

        self.participant_label = QLabel('Number of Participants')  # Ранее 'Количество клиентов'
        layout.addWidget(self.participant_label)
        self.participant_input = QLineEdit()
        layout.addWidget(self.participant_input)

        self.details_label = QLabel('Details')  # Ранее 'Блюда'
        layout.addWidget(self.details_label)
        self.details_input = QLineEdit()
        layout.addWidget(self.details_input)

        self.add_task_button = QPushButton('Add Task')  # Ранее 'Добавить заказ'
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_task(self):
        reference_number = self.reference_input.text()  # Ранее 'table_number'
        participant_count = self.participant_input.text()  # Ранее 'customers_count'
        details = self.details_input.text()  # Ранее 'items'

        if reference_number and participant_count and details:
            task = Task(
                task_reference=int(reference_number),  # Ранее 'table_number'
                participant_count=int(participant_count),  # Ранее 'customers_count'
                details=details,  # Ранее 'items'
                assignee_id=self.associate.id,  # Ранее 'waiter_id'
                status=TaskStatus.NEW  # Ранее 'pending'
            )
            session.add(task)
            session.commit()
            self.task_added.emit()  # Ранее 'order_added'
            QMessageBox.information(self, 'Task Added', 'New task successfully added.')  # Ранее 'Заказ добавлен', 'Новый заказ успешно добавлен'
            self.close()
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields are required.')  # Ранее 'Ошибка ввода', 'Все поля обязательны для заполнения'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_task_window = AddTaskWindow(None)  # Ранее 'AddOrderWindow'
    add_task_window.show()
    sys.exit(app.exec_())
