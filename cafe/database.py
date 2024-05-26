# database.py
# Этот файл отвечает за определение базы данных и инициализацию.

import os
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import enum

# Базовый класс для всех моделей
Base = declarative_base()

# URL для подключения к базе данных
DATABASE_URL = 'sqlite:///cafe.db'  # Измените на 'sqlite:///hotel.db' для отеля
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Перечисление ролей пользователей
class UserRole(enum.Enum):
    ADMIN = 'admin'
    WAITER = 'waiter'  # Измените на 'receptionist' для отеля
    CHEF = 'chef'      # Измените на 'housekeeper' для отеля

# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(String, default='active')

# Перечисление статусов заказов
class OrderStatus(enum.Enum):
    PENDING = 'pending'
    COOKING = 'cooking'  # Измените на 'cleaning' для отеля
    READY = 'ready'      # Измените на 'ready' для отеля
    PAID = 'paid'        # Измените на 'checked_out' для отеля

# Модель заказа
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    table_number = Column(Integer, nullable=False)  # Измените на 'room_number' для отеля
    customers_count = Column(Integer, nullable=False)  # Измените на 'guests_count' для отеля
    items = Column(String, nullable=False)  # Измените на 'services' для отеля
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    waiter_id = Column(Integer, ForeignKey('users.id'))  # Измените на 'receptionist_id' для отеля
    waiter = relationship('User', foreign_keys=[waiter_id])

# Ассоциация для смен
shift_assignment = Table('shift_assignment', Base.metadata,
    Column('shift_id', Integer, ForeignKey('shifts.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

# Модель смены
class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    time = Column(String, nullable=False)
    users = relationship('User', secondary=shift_assignment, back_populates='shifts')

User.shifts = relationship('Shift', secondary=shift_assignment, back_populates='users')

# Инициализация базы данных
def initialize_database():
    if not os.path.exists('cafe.db'):  # Измените на 'hotel.db' для отеля
        Base.metadata.create_all(engine)
        # Создаем начальных пользователей
        admin = User(username='admin', password='admin123', role=UserRole.ADMIN)
        waiter = User(username='waiter', password='waiter123', role=UserRole.WAITER)  # Измените на 'receptionist'
        chef = User(username='chef', password='chef123', role=UserRole.CHEF)  # Измените на 'housekeeper'
        session.add_all([admin, waiter, chef])
        session.commit()
        print("Database initialized with default users.")
    else:
        print("Database already exists.")

initialize_database()
