# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *

#Checando os argumentos de linha de comando
if __name__ == "__main__":
    print(f'Quantos argumentos: {len(sys.argv)}')
    for i, arg in enumerate(sys.argv):
        print(f"Argument: {i}: {arg}")
class Gauss(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        self.filtro_gauss = QLabel('Filtro Gauss (3x3), (5x5) ou (7x7)')
        self.filtro_gauss.adjustSize()

        self.fator_edit = QLineEdit()    
        self.fator_edit.adjustSize()
        self.fator_edit.setReadOnly(True)

        self.tipo_filtro = QPushButton('Escolha o tipo do filtro')
        self.tipo_filtro.clicked.connect(self.adiciona_filtro)
        self.button_confirma = QPushButton('Confirmar')  
        self.button_confirma.clicked.connect(self.confirma_filtro)  

        self.grid.addWidget(self.filtro_gauss, 1, 0)
        self.grid.addWidget(self.fator_edit, 1, 1)
        self.grid.addWidget(self.tipo_filtro, 2, 0)
        self.grid.addWidget(self.button_confirma, 2, 1)
        
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 350, 300) 
        self.setWindowTitle('Filtros Gauss')
        self.show()

    def adiciona_filtro(self):
        items = ("3x3", "5x5", "7x7")
        item, ok = QInputDialog.getItem(self, "Selecione o Filtro", "Lista de Filtros", items, 0, False)

        if ok and item:
            self.fator_edit.setText(str(item))

    def confirma_filtro(self):
        #Abrir os arquivos de entrada e de saída
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
        
        if (self.fator_edit.text() == "3x3"):
            #Gaussiana 3x3
            kernel = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
            kernel = np.asarray(kernel)/16
        elif (self.fator_edit.text() == "5x5"):
            #Gauss 5x5
            kernel = [[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]]
            kernel = np.asarray(kernel)/273
        elif (self.fator_edit.text() == "7x7"):
            #Gauss 7x7
            kernel = [[0,0,1,2,1,0,0],[0,3,13,22,13,3,0],[1,13,59,97,59,13,1],[2,22,97,159,97,22,2],[1,13,59,97,59,13,1],[0,3,13,22,13,3,0],[0,0,1,2,1,0,0]]
            kernel = np.asarray(kernel)/1003            
        else:
            print("Opção de filtro incorreta")

        print(kernel)

        ks = int((len(kernel) - 1) / 2)
        
        string = str(sys.argv[1])
        particao1 = string.rpartition('.')

        if (particao1[2] == 'pgm'):
            #reshape
            imagem = np.reshape(imagem, (altura, largura))   
            print("P2")
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
        elif (particao1[2] == 'ppm'):              
            #reshape
            imagem = np.reshape(imagem, (altura, largura, 3))
            print("P3")
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
    ex = Gauss()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
