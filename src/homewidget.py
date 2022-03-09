# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView
from src.avisowidget import AvisoWidget


class HomeWidget(QtWidgets.QWidget):

    def __init__(self, webScrapper):
        super(HomeWidget, self).__init__()
        uic.loadUi('src/homewidget.ui', self)
        self.webScrapper = webScrapper
        self.avisosTableView.setModel(self.webScrapper.getAvisosModel())
        self.avisosTableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.avisosTableView.hideColumn(3)

    def verAviso(self, avisoIndex):
        href = avisoIndex.siblingAtColumn(3).data()
        titulo = avisoIndex.siblingAtColumn(0).data()
        self.avisoWidget = AvisoWidget(self.webScrapper, titulo, href)
        self.avisoWidget.show()

    def setBemVindoLabel(self, title):
        self.bemVindoLabel.setText(title)
