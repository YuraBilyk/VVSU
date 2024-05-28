# specialist_interface.py
# Этот файл отвечает за интерфейс специалиста (ранее повара).

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from database import session, Task, TaskStatus

class SpecialistInterface(QMainWindow):  # Ранее 'ChefWindow'
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Specialist Panel')  # Ранее 'Панель повара'
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

        self.update_status_button = QPushButton('Update Status')  # Ранее 'Обновить статус'
        self.update_status_button.clicked.connect(self.update_task_status)
        layout.addWidget(self.update_status_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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

    def update_task_status(self):
        selected_row = self.task_table.currentRow()
        if selected_row >= 0:
            task_id = int(self.task_table.item(selected_row, 0).text())
            task = session.query(Task).get(task_id)
            if task.status == TaskStatus.IN_PROGRESS:  # Ранее 'cooking'
                task.status = TaskStatus.COMPLETED  # Ранее 'ready'
                session.commit()
                self.load_tasks()
                QMessageBox.information(self, 'Status Updated', f'Task {task.id} is now completed.')  # Ранее 'Статус заказа обновлен', 'Заказ {order.id} готов'
            elif task.status == TaskStatus.NEW:  # Ранее 'pending'
                task.status = TaskStatus.IN_PROGRESS  # Ранее 'cooking'
                session.commit()
                self.load_tasks()
                QMessageBox.information(self, 'Status Updated', f'Task {task.id} is now in progress.')  # Ранее 'Статус заказа обновлен', 'Заказ {order.id} готовится'
            else:
                QMessageBox.warning(self, 'Error', 'Only tasks in progress or new tasks can be updated.')  # Ранее 'Можно обновить только готовящиеся или ожидающие заказы'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    specialist_interface = SpecialistInterface(None)
    specialist_interface.show()
    sys.exit(app.exec_())
