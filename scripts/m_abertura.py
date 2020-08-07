# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QBasicTimer
from PyQt5.QtGui import *

class Abertura(QWidget):
    def __init__(self):
        super().__init__()        
        self.initUI()

    def initUI(self):
        self.elemento = QLabel('Elemento selecionado:')
        self.elemento.adjustSize()

        self.elemento_edit = QLineEdit()
        self.elemento_edit.adjustSize()
        self.elemento_edit.setReadOnly(True)

        self.button_elemento = QPushButton('Selecionar elemento estruturante')
        self.button_elemento.clicked.connect(self.opcao_elemento)

        self.button_confirma = QPushButton('Confirmar')
        self.button_confirma.clicked.connect(self.confirma_elemento)

        self.grid = QGridLayout()
        self.grid.setContentsMargins(15, 0, 15, 0)
        self.grid.setColumnStretch(0 , 0)
        self.grid.setColumnStretch(1 , 0)
        
        self.grid.addWidget(self.elemento, 0, 0, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.elemento_edit, 0, 1, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.button_elemento, 1, 0, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.button_confirma, 1, 1, QtCore.Qt.AlignTop)

        #self.layout.setRowStretch(0, 0)
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Abertura")
        self.show()

    def opcao_elemento(self):
        items = ("3x3", "5x5", "7x7", "9x9")
        item, ok = QInputDialog.getItem(self, "Selecione o elemento", "Lista de Elementos", items, 0, False)

        if ok and item:
            self.elemento_edit.setText(str(item))

    def confirma_elemento(self):
        opcao = self.elemento_edit.text()

        #abrir o arquivo original e a cópia
        entrada = open(sys.argv[1], "r+")
        saida = open(sys.argv[2], "w+")        
        linha = entrada.readline() # P1
        linha = entrada.readline() # Comentário
        linha = entrada.readline() # Dimensões da imagem
        dimensoes = linha.split() # Lista com as dimensões
        largura = int(dimensoes[0])
        altura = int(dimensoes[1])
        dimensoes = np.asarray(dimensoes, dtype=int) # Converte a lista para um array
        linhas = entrada.readlines() # lê todo o restante do arquivo
        linhas = [x.strip() for x in linhas] # remove o \n do final de todas as linhas

        def concatenate_list_data(list):
            result = ''
            for element in list:
                result += str(element)
            return result

        #concatena todos os elementos em uma única string
        longstring = concatenate_list_data(linhas)
        #converte a string longa para um array de uma dimensão
        image = np.array(list(longstring))
        #muda a forma do array de [altura*largura, 1] para [altura, largura]
        image = np.reshape(image, [dimensoes[1], dimensoes[0]])
        #converte a matriz para inteiro
        image = image.astype(int)

        if opcao == "3x3":
            #Elemento Estruturante 3x3
            estruturante = [[0, 0, 0], [0, 1, 0], [0, 1, 0]]
        elif opcao == "5x5":
            #Elemento Estruturante 5x5
            estruturante = [[0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [0, 1, 1, 0, 0]]
        elif opcao == "7x7":
            #Elemento Estruturante 7x7
            estruturante = [[0, 0, 0, 0, 1, 1, 1], [1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 0, 1, 1]]
        elif opcao == "9x9":
            #Elemento Estruturante 9x9
            estruturante = [[1, 1, 1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 0, 1, 1, 1], [1, 0, 0, 0, 1, 1, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]

        #Pegar pixel posição pixel central
        pixel = int((len(estruturante) - 1) / 2)

        #escrevendo a imagem cópia
        saida.write("P1\n")
        saida.write("#Criado por Gideone\n")
        saida.write(str(largura))
        saida.write(" ")
        saida.write(str(altura))
        saida.write("\n")

        image2 = image.copy()

        for i in range(pixel, len(image) - pixel):
            for j in range(pixel, len(image[1]) - pixel):
                for x in range(len(estruturante)):
                    for y in range(len(estruturante[1])):
                        if image[i][j] == 0 and estruturante[x][y] == 1:
                            image2[i - pixel + x][j - pixel + y] = 0

        image3 = image2.copy()

        for i in range(pixel, len(image2)-pixel):
            for j in range(pixel, len(image2[1])-pixel):
                for x in range(len(estruturante)):
                    for y in range(len(estruturante[1])):
                        if image2[i][j] == 1 and estruturante[x][y] == 1:
                            image3[i - pixel + x][j - pixel + y] = 1   

        for i in range(len(image3)):
            for j in range(len(image3[1])):
                saida.write(str(image3[i][j]))
                saida.write("\n")

        # fechar os dois arquivos.
        entrada.close()
        saida.close()
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = Abertura()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()



