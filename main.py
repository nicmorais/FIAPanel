# This Python file uses the following encoding: utf-8

from src.loginwidget import LoginWidget
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWidget()
    win.show()
    sys.exit(app.exec())
