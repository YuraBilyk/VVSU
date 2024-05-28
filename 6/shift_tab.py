# shift_tab.py
# Этот файл отвечает за вкладку управления сменами.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox
from database import session, Shift, User, UserRole

class ShiftTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.shift_table = QTableWidget()
        self.shift_table.setColumnCount(4)
        self.shift_table.setHorizontalHeaderLabels(['Shift ID', 'Name', 'Duration', 'Participants'])  # Ранее 'ID смены', 'Название', 'Время', 'Пользователи'
        self.shift_table.setSortingEnabled(True)
        self.load_shifts()
        layout.addWidget(self.shift_table)

        self.add_shift_button = QPushButton('Add Shift')  # Ранее 'Добавить смену'
        self.add_shift_button.clicked.connect(self.add_shift)
        layout.addWidget(self.add_shift_button)

        self.assign_user_button = QPushButton('Assign User to Shift')  # Ранее 'Назначить пользователя на смену'
        self.assign_user_button.clicked.connect(self.assign_user)
        layout.addWidget(self.assign_user_button)

        self.setLayout(layout)

    def load_shifts(self):
        self.shift_table.setRowCount(0)
        shifts = session.query(Shift).all()
        for shift in shifts:
            row_position = self.shift_table.rowCount()
            self.shift_table.insertRow(row_position)
            self.shift_table.setItem(row_position, 0, QTableWidgetItem(str(shift.id)))
            self.shift_table.setItem(row_position, 1, QTableWidgetItem(shift.name))
            self.shift_table.setItem(row_position, 2, QTableWidgetItem(shift.duration))  # Ранее 'time'
            users = ', '.join([user.username for user in shift.participants])  # Ранее 'users'
            self.shift_table.setItem(row_position, 3, QTableWidgetItem(users))

    def add_shift(self):
        shift_name, ok = QInputDialog.getText(self, 'Add Shift', 'Enter shift name:')  # Ранее 'Добавить смену', 'Введите название смены:'
        if ok and shift_name:
            shift_duration, ok = QInputDialog.getText(self, 'Add Shift', 'Enter shift duration (e.g., 09:00 - 17:00):')  # Ранее 'Введите время смены (например, 09:00 - 17:00):'
            if ok and shift_duration:
                shift = Shift(name=shift_name, duration=shift_duration)  # Ранее 'time'
                session.add(shift)
                session.commit()
                self.load_shifts()
                QMessageBox.information(self, 'Success', 'Shift added successfully.')  # Ранее 'Смена успешно добавлена'

    def assign_user(self):
        selected_row = self.shift_table.currentRow()
        if selected_row >= 0:
            shift_id = int(self.shift_table.item(selected_row, 0).text())
            shift = session.query(Shift).get(shift_id)
            users = session.query(User).filter(User.role.in_([UserRole.ASSOCIATE, UserRole.SPECIALIST])).all()  # Ранее 'waiter', 'chef'
            user_list = [user.username for user in users]
            user_name, ok = QInputDialog.getItem(self, 'Assign User to Shift', 'Select user:', user_list, 0, False)  # Ранее 'Назначить пользователя на смену', 'Выберите пользователя:'
            if ok and user_name:
                user = session.query(User).filter_by(username=user_name).first()
                if user:
                    shift.participants.append(user)  # Ранее 'users'
                    session.commit()
                    self.load_shifts()
                    QMessageBox.information(self, 'Success', f'{user.username} assigned to shift {shift.name}.')  # Ранее '{user.username} назначен на смену {shift.name}'
