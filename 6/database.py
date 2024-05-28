# database.py
# Этот файл отвечает за определение базы данных и инициализацию.

import os
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import enum

# Базовый класс для всех моделей
Base = declarative_base()

# URL для подключения к базе данных
DATABASE_URL = 'sqlite:///system.db'  # Ранее 'sqlite:///cafe.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Перечисление ролей пользователей
class UserRole(enum.Enum):
    MANAGER = 'manager'  # Ранее 'admin'
    ASSOCIATE = 'associate'  # Ранее 'waiter'
    SPECIALIST = 'specialist'  # Ранее 'chef'

# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(String, default='active')

# Перечисление статусов задач
class TaskStatus(enum.Enum):
    NEW = 'new'  # Ранее 'pending'
    IN_PROGRESS = 'in_progress'  # Ранее 'cooking'
    COMPLETED = 'completed'  # Ранее 'ready'
    FINALIZED = 'finalized'  # Ранее 'paid'

# Модель задачи/заказа
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_reference = Column(Integer, nullable=False)  # Ранее 'table_number'
    participant_count = Column(Integer, nullable=False)  # Ранее 'customers_count'
    details = Column(String, nullable=False)  # Ранее 'items'
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
    assignee_id = Column(Integer, ForeignKey('users.id'))  # Ранее 'waiter_id'
    assignee = relationship('User', foreign_keys=[assignee_id])

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
    duration = Column(String, nullable=False)  # Ранее 'time'
    participants = relationship('User', secondary=shift_assignment, back_populates='shifts')

User.shifts = relationship('Shift', secondary=shift_assignment, back_populates='participants')

# Инициализация базы данных                                                                               логи/пароль пользователей
def initialize_database():
    if not os.path.exists('system.db'):  # Ранее 'cafe.db'
        Base.metadata.create_all(engine)
        # Создаем начальных пользователей
        manager = User(username='admin', password='admin123', role=UserRole.MANAGER)
        associate = User(username='associate', password='associate123', role=UserRole.ASSOCIATE)  # Ранее 'waiter'
        specialist = User(username='specialist', password='specialist123', role=UserRole.SPECIALIST)  # Ранее 'chef'
        session.add_all([manager, associate, specialist])
        session.commit()
        print("Database initialized with default users.")
    else:
        print("Database already exists.")

initialize_database()
