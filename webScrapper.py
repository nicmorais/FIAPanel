# This Python file uses the following encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re
class Aviso:
    def __init__(self, title, isNew, href, dataAviso):
            self.title = title
            self.isNew = isNew
            self.href = href
            self.dataAviso = dataAviso

class WebScrapper:
    def __init__(self, usuario, senha):
        self.headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www2.fiap.com.br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www2.fiap.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.data = {
          'urlRedirecionamento': '',
          'usuario': usuario,
          'senha': senha
        }

    def conectar(self):

        response = requests.post('https://www2.fiap.com.br/Aluno/LogOn', headers=self.headers, data=self.data)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup = soup.find_all(class_='i-avisos-item')

        self.avisos = []

        for i in soup:
            i = i.find_all(class_='i-avisos-link')
            i = i[0]
            dataAviso = i.find(class_='i-avisos-data').string

            title = i.find(class_='i-avisos-column-title').string
            title = re.sub("\n|\r","", title)

            if(len(i['class']) == 3):
                    isNew = True
            else:
                    isNew = False
            href = "https://www2.fiap.com.br" + i['href']
            if(isNew):
                isNew = "Novo"

            self.avisos.append(Aviso(title, isNew, href, dataAviso))

    def getAvisos(self):
        self.conectar()
        return self.avisos

    def getAvisoFull(self, hrefAviso):
        return
