# waiter_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget
from database import session, Order

class WaiterWindow(QMainWindow):
    def __init__(self, waiter):
        super().__init__()
        self.setWindowTitle('Waiter Panel')
        self.setGeometry(100, 100, 600, 400)
        self.waiter = waiter
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.order_list = QListWidget()
        self.load_orders()
        layout.addWidget(self.order_list)

        self.add_order_button = QPushButton('Add Order')
        self.add_order_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_order_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_orders(self):
        self.order_list.clear()
        orders = session.query(Order).filter_by(waiter_id=self.waiter.id).all()
        for order in orders:
            self.order_list.addItem(f"Order {order.id}: Table {order.table_number}, {order.customers_count} customers, Items: {order.items}, Status: {order.status.value}")

    def add_order(self):
        from add_order_window import AddOrderWindow
        self.add_order_window = AddOrderWindow(self.waiter)
        self.add_order_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    waiter_window = WaiterWindow(None)
    waiter_window.show()
    sys.exit(app.exec_())
