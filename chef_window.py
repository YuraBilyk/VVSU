# chef_window.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget
from database import session, Order, OrderStatus

class ChefWindow(QMainWindow):
    def __init__(self, chef):
        super().__init__()
        self.setWindowTitle('Chef Panel')
        self.setGeometry(100, 100, 600, 400)
        self.chef = chef
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.order_list = QListWidget()
        self.load_orders()
        layout.addWidget(self.order_list)

        self.update_order_button = QPushButton('Update Order Status')
        self.update_order_button.clicked.connect(self.update_order_status)
        layout.addWidget(self.update_order_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_orders(self):
        self.order_list.clear()
        orders = session.query(Order).all()
        for order in orders:
            self.order_list.addItem(f"Order {order.id}: Table {order.table_number}, {order.customers_count} customers, Items: {order.items}, Status: {order.status.value}")

    def update_order_status(self):
        selected_order = self.order_list.currentItem()
        if selected_order:
            order_id = int(selected_order.text().split(' ')[1])
            order = session.query(Order).get(order_id)
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.COOKING
            elif order.status == OrderStatus.COOKING:
                order.status = OrderStatus.READY
            session.commit()
            self.load_orders()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chef_window = ChefWindow(None)
    chef_window.show()
    sys.exit(app.exec_())
