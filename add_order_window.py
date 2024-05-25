# add_order_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from database import session, Order, OrderStatus, User

class AddOrderWindow(QMainWindow):
    order_added = pyqtSignal()

    def __init__(self, waiter):
        super().__init__()
        self.setWindowTitle('Add Order')
        self.setGeometry(100, 100, 300, 200)
        self.waiter = waiter
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table_label = QLabel('Table Number')
        layout.addWidget(self.table_label)
        self.table_input = QLineEdit()
        layout.addWidget(self.table_input)

        self.customers_label = QLabel('Customers Count')
        layout.addWidget(self.customers_label)
        self.customers_input = QLineEdit()
        layout.addWidget(self.customers_input)

        self.items_label = QLabel('Items')
        layout.addWidget(self.items_label)
        self.items_input = QLineEdit()
        layout.addWidget(self.items_input)

        self.add_order_button = QPushButton('Add Order')
        self.add_order_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_order_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_order(self):
        table_number = self.table_input.text()
        customers_count = self.customers_input.text()
        items = self.items_input.text()

        if table_number and customers_count and items:
            order = Order(
                table_number=int(table_number),
                customers_count=int(customers_count),
                items=items,
                waiter_id=self.waiter.id,
                status=OrderStatus.PENDING
            )
            session.add(order)
            session.commit()
            self.order_added.emit()
            QMessageBox.information(self, 'Order Added', 'New order has been added successfully.')
            self.close()
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields are required.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_order_window = AddOrderWindow(None)
    add_order_window.show()
    sys.exit(app.exec_())
