# shift_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QInputDialog, QMessageBox
from database import session, Shift, User, UserRole

class ShiftTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.shift_list = QListWidget()
        self.load_shifts()
        layout.addWidget(self.shift_list)

        self.add_shift_button = QPushButton('Add Shift')
        self.add_shift_button.clicked.connect(self.add_shift)
        layout.addWidget(self.add_shift_button)

        self.assign_user_button = QPushButton('Assign User to Shift')
        self.assign_user_button.clicked.connect(self.assign_user)
        layout.addWidget(self.assign_user_button)

        self.setLayout(layout)

    def load_shifts(self):
        self.shift_list.clear()
        shifts = session.query(Shift).all()
        for shift in shifts:
            users = ', '.join([user.username for user in shift.users])
            self.shift_list.addItem(f"{shift.id} - {shift.name} ({shift.time}) - Users: {users}")

    def add_shift(self):
        shift_name, ok = QInputDialog.getText(self, 'Add Shift', 'Enter shift name:')
        if ok and shift_name:
            shift_time, ok = QInputDialog.getText(self, 'Add Shift', 'Enter shift time (e.g. 09:00 - 17:00):')
            if ok and shift_time:
                shift = Shift(name=shift_name, time=shift_time)
                session.add(shift)
                session.commit()
                self.load_shifts()
                QMessageBox.information(self, 'Success', 'Shift added successfully')

    def assign_user(self):
        selected_shift = self.shift_list.currentItem()
        if selected_shift:
            shift_id = int(selected_shift.text().split(' ')[0])
            shift = session.query(Shift).get(shift_id)
            users = session.query(User).filter(User.role.in_([UserRole.WAITER, UserRole.CHEF])).all()
            user_list = [user.username for user in users]
            user_name, ok = QInputDialog.getItem(self, 'Assign User', 'Select user:', user_list, 0, False)
            if ok and user_name:
                user = session.query(User).filter_by(username=user_name).first()
                if user:
                    shift.users.append(user)
                    session.commit()
                    self.load_shifts()
                    QMessageBox.information(self, 'Success', f'{user.username} assigned to {shift.name}')
