# associate_interface.py
# Этот файл отвечает за интерфейс сотрудника (ранее официант).

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from database import session, Task, TaskStatus

class AssociateInterface(QMainWindow):  # Ранее 'WaiterWindow'
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Associate Panel')  # Ранее 'Панель официанта'
        self.setGeometry(100, 100, 600, 400)
        self.user = user
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.task_table = QTableWidget()  # Ранее 'order_table'
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(['Task ID', 'Reference', 'Count', 'Details', 'Status'])  # Ранее 'ID заказа', 'Номер стола', 'Количество клиентов', 'Блюда', 'Статус'
        self.task_table.setSortingEnabled(True)
        self.load_tasks()
        layout.addWidget(self.task_table)

        self.add_task_button = QPushButton('Add Task')  # Ранее 'Добавить заказ'
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.accept_task_button = QPushButton('Start Task')  # Ранее 'Принять заказ'
        self.accept_task_button.clicked.connect(self.accept_task)
        layout.addWidget(self.accept_task_button)

        self.complete_task_button = QPushButton('Complete Task')  # Ранее 'Оплатить заказ'
        self.complete_task_button.clicked.connect(self.complete_task)
        layout.addWidget(self.complete_task_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_tasks(self):
        self.task_table.setRowCount(0)
        tasks = session.query(Task).filter_by(assignee_id=self.user.id).all()  # Ранее 'waiter_id'
        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(str(task.id)))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(str(task.task_reference)))  # Ранее 'table_number'
            self.task_table.setItem(row_position, 2, QTableWidgetItem(str(task.participant_count)))  # Ранее 'customers_count'
            self.task_table.setItem(row_position, 3, QTableWidgetItem(task.details))  # Ранее 'items'
            self.task_table.setItem(row_position, 4, QTableWidgetItem(task.status.value))

    def add_task(self):
        from add_task_window import AddTaskWindow  # Ранее 'add_order_window'
        self.add_task_window = AddTaskWindow(self.user)
        self.add_task_window.task_added.connect(self.load_tasks)
        self.add_task_window.show()

    def accept_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = int(self.task_table.item(selected_row, 0).text())
            task = session.query(Task).get(task_id)
            if task.status == TaskStatus.NEW:  # Ранее 'pending'
                task.status = TaskStatus.IN_PROGRESS  # Ранее 'cooking'
                session.commit()
                self.load_tasks()
                QMessageBox.information(self, 'Task Started', f'Task {task.id} is now in progress.')  # Ранее 'Заказ принят', 'Заказ {order.id} теперь готовится'
            else:
                QMessageBox.warning(self, 'Error', 'Only new tasks can be started.')  # Ранее 'Можно принять только ожидающие заказы'

    def complete_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = int(self.task_table.item(selected_row, 0).text())
            task = session.query(Task).get(task_id)
            if task.status == TaskStatus.IN_PROGRESS:  # Ранее 'ready'
                task.status = TaskStatus.COMPLETED  # Ранее 'paid'
                session.commit()
                self.load_tasks()
                QMessageBox.information(self, 'Task Completed', f'Task {task.id} is now completed.')  # Ранее 'Заказ оплачен', 'Заказ {order.id} был оплачен'
            else:
                QMessageBox.warning(self, 'Error', 'Only tasks in progress can be completed.')  # Ранее 'Можно оплатить только готовые заказы'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    associate_interface = AssociateInterface(None)
    associate_interface.show()
    sys.exit(app.exec_())
