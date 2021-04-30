import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import os.path
from os import path

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMessageBox, QTableWidgetItem, QLineEdit
)
from PyQt5.uic import loadUi

from webScrapper import *

class avisoFull(QDialog):
    def __init__(self, avisoContent, parent=None):
        super().__init__(parent)
        loadUi("ui/avisoFullWidget.ui", self)
        self.avisoTextBrowser.setText(avisoContent)


class FIAPanelHome(QDialog):
    def __init__(self, usuario, senha, parent=None):
        super().__init__(parent)
        loadUi("ui/home.ui", self)
        self.scrapper = WebScrapper(usuario, senha)

        self.avisosTableWidget.setRowCount(10)
        self.avisosTableWidget.setColumnCount(4)
        self.avisosTableWidget.horizontalHeader().hide()

        header = self.avisosTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.avisosTableWidget.setColumnHidden(3, True)

        row = 0
        for aviso in self.scrapper.getAvisos():
            self.avisosTableWidget.setItem(row, 0, QTableWidgetItem(aviso.dataAviso))
            self.avisosTableWidget.setItem(row, 1, QTableWidgetItem(aviso.title))
            self.avisosTableWidget.setItem(row, 2, QTableWidgetItem(aviso.isNew))
            self.avisosTableWidget.setItem(row, 3, QTableWidgetItem(aviso.href))

            row += 1

        self.avisosTableWidget.cellDoubleClicked.connect(self.getHrefAt)

    def getHrefAt(self, row, column):
        href = self.avisosTableWidget.item(row, 3).text()
        title = self.avisosTableWidget.item(row, 1).text()
        self.openAviso(href, title)

    def openAviso(self, hrefAviso, titleAviso):
        self.avisoDialog = avisoFull(self.scrapper.getAvisoFull(hrefAviso))
        self.avisoDialog.setWindowTitle(titleAviso)
        self.avisoDialog.okBtn.clicked.connect(self.avisoDialog.close)
        self.avisoDialog.show()


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
