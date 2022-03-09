# This Python file uses the following encoding: utf-8
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from src.webscrapper import WebScrapper
from src.homewidget import HomeWidget


class LoginWidget(QWidget):
    def __init__(self):
        super(LoginWidget, self).__init__()
        uic.loadUi('src/loginwidget.ui', self)

    def conectar(self):
        usuario = self.rmLineEdit.text()
        senha = self.senhaLineEdit.text()
        self.scrapper = WebScrapper()
        if self.scrapper.conectar(usuario, senha):
            self.homeWidget = HomeWidget(self.scrapper)
            self.homeWidget.webScrapper = self.scrapper
            self.homeWidget.setBemVindoLabel(self.scrapper.bemVindoTitle)
            self.homeWidget.show()
            self.close()
        else:
            errorMessage = QMessageBox(self)
            errorMessage.setWindowTitle("Erro de login")
            errorMessage.setText("Senha inválida.")
            errorMessage.setStyleSheet("color: 'white'")
            errorMessage.exec()
            self.senhaLineEdit.setFocus()
            self.senhaLineEdit.clear()
