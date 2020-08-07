# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *

class Sobel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.threshold = QLabel('Threshold:')
        self.threshold.adjustSize()

        self.threshold_edit = QLineEdit()
        self.threshold_edit.adjustSize()
        self.threshold_edit.setReadOnly(True)

        self.button_valor = QPushButton('Digite o valor')
        self.button_valor.clicked.connect(self.adiciona_valor)
        self.button_confirma = QPushButton('Confirmar')
        self.button_confirma.clicked.connect(self.confirma_threshold)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        self.grid.addWidget(self.threshold, 1, 0)
        self.grid.addWidget(self.threshold_edit, 1, 1)
        self.grid.addWidget(self.button_valor, 2, 0)
        self.grid.addWidget(self.button_confirma, 2, 1)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 350, 300) 
        self.setWindowTitle('Filtro Sobel')
        self.show()

    def adiciona_valor(self):
        num,ok = QInputDialog.getDouble(self,"Filtro Sobel","Valor")		
        if ok:
            self.threshold_edit.setText(str(num))

    def confirma_threshold(self):     
        #Recebendo valor digitado pelo usuario
        valor = self.threshold_edit.text()
        valor = float(valor) 

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
        string = str(sys.argv[1])
        self.particao1 = string.rpartition('.')

        if (self.particao1[2] == 'pgm'):
            #reshape
            imagem = np.reshape(imagem, (altura, largura))

            #Sobel
            kernelx = [[-1,0,1],[2,0,-2],[1,0,-1]]
            kernelx = np.asarray(kernelx)
            kernely = [[1,2,1],[0,0,0],[-1,-2,-1]]
            kernely = np.asarray(kernely)

            ks = int((len(kernelx)-1)/2)

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
                    sumx = 0
                    sumy = 0
                    for ki in range(len(kernelx)):
                        for kj in range(len(kernelx[1])):
                            sumx = sumx + (imagem[i-ks+ki][j-ks+kj]*kernelx[ki][kj])
                            sumy = sumy + (imagem[i-ks+ki][j-ks+kj]*kernely[ki][kj])
                    sumxy = math.sqrt((sumx**2)+(sumy**2))
                    #Threshold
                    sum = max(sumxy, valor) 
                    sum = int(sum) if sum != valor else 0
                    sum = str(sum)
                    saida.write(sum)
                    saida.write("\n")
                    
        elif (self.particao1[2] == 'ppm'):
            #reshape
            imagem = np.reshape(imagem, (altura, largura, 3))

            #Sobel
            kernelx = [[-1,0,1],[2,0,-2],[1,0,-1]]
            kernelx = np.asarray(kernelx)
            kernely = [[1,2,1],[0,0,0],[-1,-2,-1]]
            kernely = np.asarray(kernely)
            ks = int((len(kernelx)-1)/2) 

            #escrevendo a imagem cópia
            saida.write("P3\n")
            saida.write("#Criado por Gideone\n")
            saida.write(str(largura-(ks*2)))
            saida.write(" ")
            saida.write(str(altura-(ks*2)))
            saida.write("\n")
            saida.write("255\n")

            #fazer a transformação
            for i in range(ks, len(imagem)-ks):
                for j in range(ks, len(imagem[1])-ks):
                    for k in range(3):
                        sumx = 0
                        sumy = 0
                        for ki in range(len(kernelx)):
                            for kj in range(len(kernelx[1])):
                                sumx = sumx + (imagem[i-ks+ki][j-ks+kj][k]*kernelx[ki][kj])
                                sumy = sumy + (imagem[i-ks+ki][j-ks+kj][k]*kernely[ki][kj])
                        sumxy = math.sqrt((sumx**2)+(sumy**2))
                        #Threshold
                        sum = max(sumxy, valor)
                        sum = int(sum) if sum != valor else 0
                        sum = str(sum)
                        saida.write(sum)
                        saida.write("\n")            
        #fechar os dois arquivos.
        entrada.close()
        saida.close()
        self.close()
def main():
    app = QApplication(sys.argv)
    ex = Sobel()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
