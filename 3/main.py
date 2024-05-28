# main.py
import sys
from PyQt5.QtWidgets import QApplication
from login import LoginWindow

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()




# Установка необходимых библиотек
# pip install PyQt5 SQLAlchemy