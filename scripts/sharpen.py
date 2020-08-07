# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *

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

#Sharpen
kernel = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
kernel = np.asarray(kernel)

print(kernel)

ks = int((len(kernel) - 1) / 2)

string = str(sys.argv[1])
particao1 = string.rpartition('.')
if (particao1[2] == 'pgm'):
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
elif (particao1[2] == 'ppm'):
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
    #fazer a cópia
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
else:
    self.erro_message() 
    
#fechar os dois arquivos.
entrada.close()
saida.close()

def erro_message(self):
    self.error = QMessageBox()
    self.error.setIcon(QMessageBox.Warning)
    self.error.setWindowTitle("ERRO")
    self.error.setText("Apenas arquivos PGM OU PPM")
    self.error.setStandardButtons(QMessageBox.Ok)
    self.error.exec_()