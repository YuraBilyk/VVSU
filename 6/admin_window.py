# manager_interface.py
# Этот файл отвечает за интерфейс менеджера.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from user_tab import UserTab  # Ранее 'employee_tab'
from task_tab import TaskTab  # Ранее 'order_tab'
from shift_tab import ShiftTab

class ManagerInterface(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Manager Panel')  # Ранее 'Панель администратора'
        self.setGeometry(100, 100, 800, 600)
        self.user = user
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        
        self.user_tab = UserTab()  # Ранее 'EmployeeTab'
        self.tabs.addTab(self.user_tab, 'Users')  # Ранее 'Сотрудники'
        
        self.task_tab = TaskTab()  # Ранее 'OrderTab'
        self.tabs.addTab(self.task_tab, 'Tasks')  # Ранее 'Заказы'

        self.shift_tab = ShiftTab()
        self.tabs.addTab(self.shift_tab, 'Shifts')  # Ранее 'Смены'
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager_interface = ManagerInterface(None)
    manager_interface.show()
    sys.exit(app.exec_())
