# admin_window.py
# Этот файл отвечает за интерфейс администратора с вкладками для управления сотрудниками, заказами и сменами.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from employee_tab import EmployeeTab
from order_tab import OrderTab
from shift_tab import ShiftTab

class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Admin Panel')
        self.setGeometry(100, 100, 800, 600)
        self.user = user
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        
        self.employee_tab = EmployeeTab()
        self.tabs.addTab(self.employee_tab, 'Employees')
        
        self.order_tab = OrderTab()
        self.tabs.addTab(self.order_tab, 'Orders')

        self.shift_tab = ShiftTab()
        self.tabs.addTab(self.shift_tab, 'Shifts')
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_window = AdminWindow(None)
    admin_window.show()
    sys.exit(app.exec_())


# AdminWindow: Основное окно администратора, которое содержит вкладки для управления сотрудниками, заказами и сменами.
# QTabWidget: Виджет для создания вкладок. Добавьте свои вкладки для отеля, например, "Bookings" и "Staff Schedules".