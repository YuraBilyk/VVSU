# task_tab.py
# Этот файл отвечает за вкладку управления задачами.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from database import session, Task

class TaskTab(QWidget):  # Ранее 'OrderTab'
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.task_table = QTableWidget()  # Ранее 'order_table'
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(['Task ID', 'Reference', 'Count', 'Details', 'Status'])  # Ранее 'ID заказа', 'Номер стола', 'Количество клиентов', 'Блюда', 'Статус'
        self.task_table.setSortingEnabled(True)
        self.load_tasks()
        layout.addWidget(self.task_table)

        self.setLayout(layout)

    def load_tasks(self):
        self.task_table.setRowCount(0)
        tasks = session.query(Task).all()
        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(str(task.id)))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(str(task.task_reference)))  # Ранее 'table_number'
            self.task_table.setItem(row_position, 2, QTableWidgetItem(str(task.participant_count)))  # Ранее 'customers_count'
            self.task_table.setItem(row_position, 3, QTableWidgetItem(task.details))  # Ранее 'items'
            self.task_table.setItem(row_position, 4, QTableWidgetItem(task.status.value))
