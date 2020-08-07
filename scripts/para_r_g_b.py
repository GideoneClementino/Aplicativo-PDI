# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QBasicTimer
from PyQt5.QtGui import *

class Rgb(QWidget):
    def __init__(self):
        super().__init__()        
        self.initUI()
    def initUI(self):
        self.camada = QLabel('Camada selecionada:')
        self.camada.adjustSize()             

        self.camada_edit = QLineEdit()
        #self.camada_r_edit.setFixedWidth(150)
        self.camada_edit.setReadOnly(True)
            
        self.button_adicionar_camada = QPushButton("Selecionar camada")
        self.button_adicionar_camada.clicked.connect(self.opcao_camada)

        self.button_confirma = QPushButton("Confirmar")
        self.button_confirma.clicked.connect(self.confirma_separacao)

        self.grid = QGridLayout()
        self.grid.setContentsMargins(15, 0, 15, 0)
        self.grid.setColumnStretch(0 , 0)
        self.grid.setColumnStretch(1 , 0)
        
        self.grid.addWidget(self.camada, 0, 0, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.camada_edit, 0, 1, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.button_adicionar_camada, 1, 0, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.button_confirma, 1, 1, QtCore.Qt.AlignTop)

        #self.layout.setRowStretch(0, 0)
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Separação R_G_B")
        self.show()

    def opcao_camada(self):
        items = ("Camada R", "Camada G", "Camada B")
        item, ok = QInputDialog.getItem(self, "Selecione a camada", "Lista de Camadas", items, 0, False)

        if ok and item:
            self.camada_edit.setText(str(item))

    def confirma_separacao(self):
        opcao = self.camada_edit.text()

        #abrir o arquivo original e a cópia
        entrada = open(sys.argv[1], "r+")
        saida = open(sys.argv[2], "w+")
        linha = entrada.readline() #P3
        linha = entrada.readline() #Comentário
        linha = entrada.readline() #Dimensões
        dimensoes = linha.split()
        largura = int(dimensoes[0])
        altura = int(dimensoes[1])
        linha = entrada.readline() #Valor fixo
        linha = entrada.readlines() #Ler o restante do arquivo e grava como lista

        #converter de lista para array
        imagem = np.asarray(linha, dtype=int)
        #reshape
        imagem = np.reshape(imagem, (altura, largura, 3))

        #escrevendo a imagem cópia
        saida.write("P3\n")
        saida.write("#Criado por Gideone\n")
        saida.write(str(largura))
        saida.write(" ")
        saida.write(str(altura))
        saida.write("\n")
        saida.write("255\n")

        if opcao == "Camada R":
            #fazer a cópia
            for i in range(0, len(imagem)):
                for j in range(0, len(imagem[1])):
                    r = imagem[i][j][0]
                    g = 0
                    b = 0
                    msg = str(r) + " " + str(g) + " " + str(b)
                    saida.write(msg)
                    saida.write("\n")
        elif opcao == "Camada G":
            #fazer a cópia
            for i in range(0, len(imagem)):
                for j in range(0, len(imagem[1])):
                    r = 0
                    g = imagem[i][j][0]
                    b = 0
                    msg = str(r) + " " + str(g) + " " + str(b)
                    saida.write(msg)
                    saida.write("\n")     
        elif opcao == "Camada B":
            #fazer a cópia
            for i in range(0, len(imagem)):
                for j in range(0, len(imagem[1])):
                    r = 0
                    g = 0
                    b = imagem[i][j][0]
                    msg = str(r) + " " + str(g) + " " + str(b)
                    saida.write(msg)
                    saida.write("\n")                                       
        #fechar os dois arquivos.
        entrada.close()
        saida.close()
        self.close()                
def main():
    app = QApplication(sys.argv)
    ex = Rgb()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
