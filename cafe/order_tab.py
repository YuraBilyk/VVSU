# order_tab.py
# Этот файл отвечает за вкладку управления заказами.

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


# load_orders: Загружает список всех заказов из базы данных.
# order_list: Список заказов, отображаемых в интерфейсе. Для отеля измените поля на room_number, guests_count и services.