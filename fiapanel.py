import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import os.path
from os import path

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMessageBox, QTableWidgetItem, QLineEdit
)
from PyQt5.uic import loadUi

from webScrapper import *

class FIAPanelHome(QDialog):
    def __init__(self, usuario, senha, parent=None):
        super().__init__(parent)
        loadUi("ui/home.ui", self)
        scrapper = WebScrapper(usuario, senha)

        self.avisosTableWidget.setRowCount(10)
        self.avisosTableWidget.setColumnCount(4)
        self.avisosTableWidget.horizontalHeader().hide()
        row = 0

        header = self.avisosTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.avisosTableWidget.setColumnHidden(3, True)

        for aviso in scrapper.getAvisos():
            self.avisosTableWidget.setItem(row, 0, QTableWidgetItem(aviso.dataAviso))
            self.avisosTableWidget.setItem(row, 1, QTableWidgetItem(aviso.title))
            self.avisosTableWidget.setItem(row, 2, QTableWidgetItem(aviso.isNew))
            self.avisosTableWidget.setItem(row, 3, QTableWidgetItem(aviso.href))

            row += 1

class FIAPanelLogin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/form.ui", self)
        self.senhaLineEdit.setEchoMode(QLineEdit.Password)
        self.conectarBtn.clicked.connect(self.conectar)

        try:
            ultimoUsuario = open("ultimoUsuario", "x")
        except:
            with open("ultimoUsuario") as file:
                try:
                    ultimoUsuario = file.readlines()[0]
                except:
                    pass
                else:
                    self.usuarioLineEdit.setText(ultimoUsuario)

    def conectar(self):
        self.showHome()

    def showHome(self):
        usuario = self.usuarioLineEdit.text()
        senha = self.senhaLineEdit.text()

        with open('ultimoUsuario', 'w') as writer:
            writer.write(usuario)

        self.home = FIAPanelHome(usuario, senha)
        self.home.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FIAPanelLogin()
    win.show()

    sys.exit(app.exec())
