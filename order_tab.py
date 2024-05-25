# order_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget
from database import session, Order

class OrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.order_list = QListWidget()
        self.load_orders()
        layout.addWidget(self.order_list)

        self.setLayout(layout)

    def load_orders(self):
        self.order_list.clear()
        orders = session.query(Order).all()
        for order in orders:
            self.order_list.addItem(f"Order {order.id}: Table {order.table_number}, {order.customers_count} customers, Items: {order.items}, Status: {order.status.value}")
