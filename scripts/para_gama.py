# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QBasicTimer
from PyQt5.QtGui import *

class Gama(QWidget):
    def __init__(self):
        super().__init__()        
        self.initUI()

    def initUI(self):
        self.fator_gama = QLabel('Fator Gama:')
        self.fator_gama.adjustSize()

        self.fator_edit = QLineEdit()    
        self.fator_edit.adjustSize()
        self.fator_edit.setReadOnly(True)

        self.button_valor = QPushButton('Digite o valor')
        self.button_valor.clicked.connect(self.adiciona_valor)
        self.button_confirma = QPushButton('Confirmar')  
        self.button_confirma.clicked.connect(self.confirma_gama)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        self.grid.addWidget(self.fator_gama, 1, 0)
        self.grid.addWidget(self.fator_edit, 1, 1)
        self.grid.addWidget(self.button_valor, 2, 0)
        self.grid.addWidget(self.button_confirma, 2, 1)
        
        self.setLayout(self.grid)
        self.setGeometry(300, 300, 350, 300) 
        self.setWindowTitle('Filtro Gama')
        self.show()

    def adiciona_valor(self):
        num,ok = QInputDialog.getDouble(self,"Filtro Gama","Valor")		
        if ok:
            self.fator_edit.setText(str(num))
             
    def confirma_gama(self, event):
        #Recebendo valor digitado pelo usuario
        gama = self.fator_edit.text()
        gama = float(gama)
        
        #Abrir os arquivos de entrada e de saída
        entrada = open(sys.argv[1], "r+")
        saida = open(sys.argv[2], "w+")
        linha = entrada.readline() #P2
        linha = entrada.readline() #comentário
        linha = entrada.readline() #Dimensões
        dimensoes = linha.split()
        largura = dimensoes[0]
        altura = dimensoes[1]
        linha = entrada.readline() #Valor fixo
        linha = entrada.readlines() # ler o restante do arquivo e grava como lista

        #converter de lista para array
        imagem = np.asarray(linha, dtype=int)
        
        string = str(sys.argv[1])
        self.particao1 = string.rpartition('.')

        if (self.particao1[2] == 'pgm'):
            #escrevendo a imagem cópia
            saida.write("P2\n")
            saida.write("#Criado por Gideone\n")
            saida.write(str(largura))
            saida.write(" ")
            saida.write(str(altura))
            saida.write("\n")
            saida.write("255\n")
        elif (self.particao1[2] == 'ppm'):
            #escrevendo a imagem cópia
            saida.write("P3\n")
            saida.write("#Criado por Gideone\n")
            saida.write(str(largura))
            saida.write(" ")
            saida.write(str(altura))
            saida.write("\n")
            saida.write("255\n")     
        else:
            self.erro_message()

        #Aplicando filtro gama
        for i in range((len(imagem))):
            n = int(((imagem[i]/255)**gama)*255)
            n = str(n)
            saida.write(n) 
            saida.write("\n")
            
        #fechar os dois arquivos e janela
        entrada.close()
        saida.close()
        self.close()

    def erro_message(self):
        self.error = QMessageBox()
        self.error.setIcon(QMessageBox.Warning)
        self.error.setWindowTitle("ERRO")
        self.error.setText("Apenas arquivos PGM OU PPM")
        self.error.setStandardButtons(QMessageBox.Ok)
        self.error.exec_()   
        
def main():
    app = QApplication(sys.argv)
    ex = Gama()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()


''' self.dica = QMessageBox() >>
    self.dica.setIcon(QMessageBox.Information)
    self.dica.setWindowTitle("Dica")
    self.dica.setText("Você abriu uma imagem em escala de cinza")
    self.dica.setStandardButtons(QMessageBox.Ok)  
    self.dica.exec_()
'''    