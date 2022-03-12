# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from src.avisowidget import AvisoWidget


class HomeWidget(QtWidgets.QWidget):
    ultimoAviso = ''

    def __init__(self, webScrapper):
        super(HomeWidget, self).__init__()
        uic.loadUi('src/homewidget.ui', self)
        self.webScrapper = webScrapper

        self.tabWidget.setTabIcon(0, QtGui.QIcon('assets/trabalhos.png'))
        self.tabWidget.setTabIcon(1, QtGui.QIcon('assets/avisos.png'))
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))

        self.icon = QSystemTrayIcon(self)
        self.icon.showMessage("Teste", "Teste", QSystemTrayIcon.Information, 10000)
        self.icon.setIcon(QIcon('assets/icon.svg'))
        self.icon.show()
        self.setUpTableView()

    def onTableViewDoubleClicked(self, avisoIndex):
        if self.tabWidget.currentIndex() == 1:
            href = avisoIndex.siblingAtColumn(3).data()
            titulo = avisoIndex.siblingAtColumn(0).data()
            self.avisoWidget = AvisoWidget(self.webScrapper, titulo, href)
            self.avisoWidget.show()

    def setBemVindoLabel(self, title):
        self.bemVindoLabel.setText(title)

    def atualizar(self):
        self.atualizandoLabel.setText('Atualizando...')
        self.setUpTableView()
        self.atualizandoLabel.setText('Atualizado')

    def setUpTableView(self):
        columnsStretch = [0, 1]
        if self.tabWidget.currentIndex() == 0:
            self.tableView.setModel(self.webScrapper.getTrabalhosModel())
        else:
            self.tableView.setModel(self.webScrapper.getAvisosModel())
            self.tableView.hideColumn(3)
            self.ultimoAviso = self.tableView.model().index(0, 0).data()

        if self.tableView.model().rowCount() > 0:
            for column in columnsStretch:
                self.tableView.horizontalHeader().setSectionResizeMode(column, QHeaderView.Stretch)
