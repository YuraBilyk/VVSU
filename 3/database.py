# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

# Создание базового класса для всех классов ORM
Base = declarative_base()
DATABASE_URL = 'sqlite:///universal.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Определение ролей пользователей в системе
class UserRole(enum.Enum):
    ADMIN = 'admin'
    ROLE1 = 'role1'  # Замените 'role1' на конкретную роль, например, 'mechanic'
    ROLE2 = 'role2'  # Замените 'role2' на конкретную роль, например, 'diagnostician'

# Определение таблицы пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(String, default='active')

# Определение статусов задач
class TaskStatus(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'В процессе'
    COMPLETED = 'completed'
    CLOSED = 'closed'

# Определение таблицы задач
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Общий заголовок задачи
    description = Column(String, nullable=False)  # Общая информация о задаче
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    user1_id = Column(Integer, ForeignKey('users.id'))  # ID пользователя роли ROLE1
    user2_id = Column(Integer, ForeignKey('users.id'))  # ID пользователя роли ROLE2
    user1 = relationship('User', foreign_keys=[user1_id])
    user2 = relationship('User', foreign_keys=[user2_id])

# Ассоциативная таблица для связи пользователей и смен
shift_user_association = Table('shift_user', Base.metadata,
    Column('shift_id', Integer, ForeignKey('shifts.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

# Определение таблицы смен
class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    time = Column(String, nullable=False)
    users = relationship('User', secondary=shift_user_association, back_populates='shifts')

User.shifts = relationship('Shift', secondary=shift_user_association, back_populates='users')

# Инициализация базы данных
def initialize_database():
    if not os.path.exists('universal.db'):
        Base.metadata.create_all(engine)
        admin = User(username='admin', password='admin123', role=UserRole.ADMIN)
        user1 = User(username='user1', password='user123', role=UserRole.ROLE1)
        user2 = User(username='user2', password='user123', role=UserRole.ROLE2)
        session.add_all([admin, user1, user2])
        session.commit()
        print("Database initialized with default users.")
    else:
        print("Database already exists.")

initialize_database()
