# This Python file uses the following encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class Aviso:
    def __init__(self, title, isNew, href, dataAviso):
        self.title = title
        self.isNew = isNew
        self.href = href
        self.dataAviso = dataAviso


class WebScrapper:
    LOGIN_URL = 'https://www2.fiap.com.br/Aluno/LogOn'
    bemVindoTitle = ''
    session = requests.Session()

    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www2.fiap.com.br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www2.fiap.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    def conectar(self, usuario, senha):
        self.data = {
          'urlRedirecionamento': '',
          'usuario': usuario,
          'senha': senha
        }

        self.response = self.session.post(self.LOGIN_URL,
                                          headers=self.headers,
                                          data=self.data)

        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        tags_invalido = self.soup.find_all(class_='a-login-error')
        if len(tags_invalido) == 0:
            bemVindoResultSet = self.soup.find_all(class_='l-header-title')
            bemVindoTitle = bemVindoResultSet[0].contents[0]
            self.bemVindoTitle = str(bemVindoTitle).strip()
            return True
        else:
            return False

    def getAvisosList(self):
        avisos = []

        avisos_soup = self.soup.find_all(class_='i-avisos-item')

        for aviso in avisos_soup:
            aviso = aviso.find_all(class_='i-avisos-link')
            aviso = aviso[0]
            dataAviso = aviso.find(class_='i-avisos-data').string

            title = aviso.find(class_='i-avisos-column-title').string
            title = re.sub('\n|\r', '', title)

            if(len(aviso['class']) == 3):
                isNew = True
            else:
                isNew = False
            href = 'https://www2.fiap.com.br' + (aviso['href'])

            avisos.append(Aviso(title, isNew, href, dataAviso))
        return avisos

    def getAvisosModel(self):
        avisosModel = QStandardItemModel()

        linha = 0
        coluna = 0
        for aviso in self.getAvisosList():
            isNew = ''
            if aviso.isNew:
                isNew = 'Novo'

            avisoAttributes = [aviso.title,
                               aviso.dataAviso,
                               isNew,
                               aviso.href]
            for avisoAttribute in avisoAttributes:
                avisoItem = QStandardItem(avisoAttribute)
                avisosModel.setItem(linha, coluna, avisoItem)
                coluna += 1
            linha += 1
            coluna = 0
        return avisosModel

    def getAvisoFull(self, hrefAviso):
        avisoFull = self.session.post(hrefAviso, data=self.data)
        avisoParsed = BeautifulSoup(avisoFull.text, 'html.parser')
        avisoText = avisoParsed.find_all("div")[0].text
        return avisoText
