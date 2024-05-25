# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

Base = declarative_base()
DATABASE_URL = 'sqlite:///cafe.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class UserRole(enum.Enum):
    ADMIN = 'admin'
    WAITER = 'waiter'
    CHEF = 'chef'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(String, default='active')

class OrderStatus(enum.Enum):
    PENDING = 'pending'
    COOKING = 'cooking'
    READY = 'ready'
    PAID = 'paid'

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    table_number = Column(Integer, nullable=False)
    customers_count = Column(Integer, nullable=False)
    items = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    waiter_id = Column(Integer, ForeignKey('users.id'))
    waiter = relationship('User', foreign_keys=[waiter_id])

def initialize_database():
    if not os.path.exists('cafe.db'):
        Base.metadata.create_all(engine)
        # Создаем начальных пользователей
        admin = User(username='admin', password='admin123', role=UserRole.ADMIN)
        waiter = User(username='waiter', password='waiter123', role=UserRole.WAITER)
        chef = User(username='chef', password='chef123', role=UserRole.CHEF)
        session.add_all([admin, waiter, chef])
        session.commit()
        print("Database initialized with default users.")
    else:
        print("Database already exists.")

initialize_database()
