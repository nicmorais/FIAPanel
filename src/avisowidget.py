# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5 import uic


class AvisoWidget(QtWidgets.QWidget):
    def __init__(self, webScrapper, tituloAviso, hrefAviso):
        super(AvisoWidget, self).__init__()
        uic.loadUi('src/avisowidget.ui', self)
        self.setWindowTitle(tituloAviso)
        bodyAviso = webScrapper.getAvisoFull(hrefAviso)
        self.textEdit.setText(bodyAviso)
