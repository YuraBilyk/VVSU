# waiter_window.py
# Этот файл отвечает за интерфейс официанта (или рецепциониста для отеля).

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QMessageBox
from database import session, Order, OrderStatus

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

        self.accept_order_button = QPushButton('Accept Order')
        self.accept_order_button.clicked.connect(self.accept_order)
        layout.addWidget(self.accept_order_button)

        self.pay_order_button = QPushButton('Pay Order')
        self.pay_order_button.clicked.connect(self.pay_order)
        layout.addWidget(self.pay_order_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_orders(self):
        self.order_list.clear()
        orders = session.query(Order).filter_by(waiter_id=self.waiter.id).all()  # Измените на receptionist_id для отеля
        for order in orders:
            self.order_list.addItem(f"Order {order.id}: Table {order.table_number}, {order.customers_count} customers, Items: {order.items}, Status: {order.status.value}")

    def add_order(self):
        from add_order_window import AddOrderWindow
        self.add_order_window = AddOrderWindow(self.waiter)
        self.add_order_window.order_added.connect(self.load_orders)
        self.add_order_window.show()

    def extract_order_id(self, order_text):
        return int(order_text.split(':')[0].split(' ')[1])

    def accept_order(self):
        selected_order = self.order_list.currentItem()
        if selected_order:
            order_id = self.extract_order_id(selected_order.text())
            order = session.query(Order).get(order_id)
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.COOKING  # Измените на 'cleaning' для отеля
                session.commit()
                self.load_orders()
                QMessageBox.information(self, 'Order Accepted', f'Order {order.id} is now being cooked.')  # Измените сообщение для отеля
            else:
                QMessageBox.warning(self, 'Error', 'Only pending orders can be accepted.')

    def pay_order(self):
        selected_order = self.order_list.currentItem()
        if selected_order:
            order_id = self.extract_order_id(selected_order.text())
            order = session.query(Order).get(order_id)
            if order.status == OrderStatus.READY:
                order.status = OrderStatus.PAID  # Измените на 'checked_out' для отеля
                session.commit()
                self.load_orders()
                QMessageBox.information(self, 'Order Paid', f'Order {order.id} has been paid.')  # Измените сообщение для отеля
            else:
                QMessageBox.warning(self, 'Error', 'Only ready orders can be marked as paid.')  # Измените сообщение для отеля

if __name__ == '__main__':
    app = QApplication(sys.argv)
    waiter_window = WaiterWindow(None)
    waiter_window.show()
    sys.exit(app.exec_())


# load_orders: Загружает список всех заказов, связанных с текущим пользователем (официантом).
# add_order: Открывает окно добавления нового заказа и обновляет список заказов после добавления.
# accept_order: Изменяет статус выбранного заказа на "готовится". В отеле измените на "убирается".
# pay_order: Изменяет статус выбранного заказа на "оплачен". В отеле измените на "выселен".