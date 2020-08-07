# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QBasicTimer
from PyQt5.QtGui import *

class Edge(QWidget):
    def __init__(self):
        super().__init__()        
        self.initUI()

    def initUI(self):    
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 15, 0, 135)    

        self.filtro_1 = QLabel('Filtro 1:')
        self.filtro_1.adjustSize()
        self.filtro_1.setAlignment(QtCore.Qt.AlignCenter)

        self.filtro_2 = QLabel('Filtro 2:')
        self.filtro_2.adjustSize()
        self.filtro_2.setAlignment(QtCore.Qt.AlignCenter)

        self.filtro_3 = QLabel('Filtro 3:')
        self.filtro_3.adjustSize()
        self.filtro_3.setAlignment(QtCore.Qt.AlignCenter)

        self.filtro_opcao = QLabel('Filtro escolhido:')
        self.filtro_opcao.adjustSize()
        self.filtro_opcao.setAlignment(QtCore.Qt.AlignCenter)

        self.filtro_edit = QLineEdit()    
        self.filtro_edit.adjustSize()
        self.filtro_edit.setReadOnly(True)
               
        self.button_opcao = QPushButton("Escolha o filtro")
        self.button_opcao.clicked.connect(self.escolhe_filtro)

        self.button_opcao_confirma = QPushButton("Confirmar")
        self.button_opcao_confirma.clicked.connect(self.confirma_filtro)
         
        #Criando as imagems (QLbabel)
        self.imagem1 = QLabel(self)
        self.endereco1 = 'images/Filtro1.PNG'
        self.pixmap1 = QtGui.QPixmap(self.endereco1)
        self.pixmap1 = self.pixmap1.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
        self.imagem1.setPixmap(self.pixmap1)
        self.imagem1.setAlignment(QtCore.Qt.AlignCenter) 

        self.imagem2 = QLabel(self)
        self.endereco2 = 'images/Filtro2.PNG'
        self.pixmap2 = QtGui.QPixmap(self.endereco2)
        self.pixmap2 = self.pixmap1.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
        self.imagem2.setPixmap(self.pixmap2)
        self.imagem2.setAlignment(QtCore.Qt.AlignCenter) 

        self.imagem3 = QLabel(self)
        self.endereco3 = 'images/Filtro3.PNG'
        self.pixmap3 = QtGui.QPixmap(self.endereco3)
        self.pixmap3 = self.pixmap3.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
        self.imagem3.setPixmap(self.pixmap3)
        self.imagem3.setAlignment(QtCore.Qt.AlignCenter) 

        self.grid.addWidget(self.filtro_1, 0, 1, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.filtro_2, 0, 2, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.filtro_3, 0, 3, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.imagem1, 1, 1)
        self.grid.addWidget(self.imagem2, 1, 2)
        self.grid.addWidget(self.imagem3, 1, 3)
        self.grid.addWidget(self.button_opcao, 2, 2, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.button_opcao_confirma, 4, 2, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.filtro_edit, 3, 2, QtCore.Qt.AlignVCenter)
        self.grid.addWidget(self.filtro_opcao, 3, 1, QtCore.Qt.AlignRight)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 350, 300) 
        self.setWindowTitle('Detecção de Bordas')
        self.show()
    def escolhe_filtro(self):
        items = ("Filtro 1", "Filtro 2", "Filtro 3")
        item, ok = QInputDialog.getItem(self, "Selecione o Filtro", "Lista de Filtros", items, 0, False)

        if ok and item:
            self.filtro_edit.setText(str(item))
    
    def confirma_filtro(self):
        self.filtro = self.filtro_edit.text()

        #Abrir os arquivos de entrada e de saída
        entrada = open(sys.argv[1], "r+")
        saida = open(sys.argv[2], "w+")
        linha = entrada.readline() #P2
        linha = entrada.readline() #Comentário
        linha = entrada.readline() #Dimensões
        dimensoes = linha.split()
        largura = int(dimensoes[0])
        altura = int(dimensoes[1])
        linha = entrada.readline() #Valor fixo
        linha = entrada.readlines() #Ler o restante do arquivo e grava como lista

        #converter de lista para array
        imagem = np.asarray(linha, dtype=int)

        if self.filtro == "Filtro 1":
            #Edge Detection
            kernel = [[1, 0, -1], [0, 0, 0],[-1, 0, 1]]

        elif self.filtro == "Filtro 2":
            #Edge Detection
            kernel = [[0, 1, 0], [1, -4, 1],[0, 1, 0]]
        elif self.filtro == "Filtro 3":
            #Edge Detection
            kernel = [[-1, -1, -1], [-1, 8, -1],[-1, -1, -1]]    
        else:
            print("Filtro incorreto")
            self.close()

        kernel = np.asarray(kernel)
        ks = int((len(kernel)-1)/2)

        string = str(sys.argv[1])
        self.particao1 = string.rpartition('.')
        if self.particao1[2] == 'pgm':
            #reshape
            imagem = np.reshape(imagem, (altura, largura))            
            #escrevendo a imagem cópia
            saida.write("P2\n")
            saida.write("#Criado por Gideone\n")
            saida.write(str(largura-(ks*2)))
            saida.write(" ")
            saida.write(str(altura-(ks*2)))
            saida.write("\n")
            saida.write("255\n")

            #fazer a transformação
            for i in range(ks, len(imagem)-ks):
                for j in range(ks, len(imagem[1])-ks):
                    sum = 0
                    for ki in range(len(kernel)):
                        for kj in range(len(kernel[1])):
                            sum = sum + (imagem[i-ks+ki][j-ks+kj]*kernel[ki][kj])
                    sum = int(sum)
                    sum = str(sum)
                    saida.write(sum)
                    saida.write("\n")

        elif self.particao1[2] == 'ppm':
            #reshape
            imagem = np.reshape(imagem, (altura, largura, 3))
            #escrevendo a imagem cópia
            saida.write("P3\n")
            saida.write("#Criado por Gideone\n")
            saida.write(str(largura-(ks*2)))
            saida.write(" ")
            saida.write(str(altura-(ks*2)))
            saida.write("\n")
            saida.write("255\n")

            for i in range(ks, len(imagem)-ks):
                for j in range(ks, len(imagem[1])-ks):
                    for k in range(3):
                        sum = 0
                        for ki in range(len(kernel)):
                            for kj in range(len(kernel[1])):
                                    sum = sum + (imagem[i - ks + ki][j - ks + kj][k] * kernel[ki][kj])
                        sum = int(sum)
                        sum = str(sum)
                        saida.write(sum)
                        saida.write("\n")    

        #fechar os dois arquivos.
        entrada.close()
        saida.close()
        self.close()        
        
def main():
    app = QApplication(sys.argv)
    ex = Edge()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()