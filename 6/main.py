# main.py
# Основной файл для запуска приложения.

import sys
from PyQt5.QtWidgets import QApplication
from login_interface import LoginInterface  # Ранее 'login_window'

def main():
    app = QApplication(sys.argv)
    login_interface = LoginInterface()
    login_interface.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
