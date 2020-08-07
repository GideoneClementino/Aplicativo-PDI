# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
#Abrir os arquivos de entrada e de saída
entrada = open(sys.argv[1], "r+")
saida = open(sys.argv[2], "w+")
linha = entrada.readline() #P3
linha = entrada.readline() #Comentário
linha = entrada.readline() #Dimensões
dimensoes = linha.split()
linha = entrada.readline() #Valor fixo
dimensoes = np.array(dimensoes, dtype=int)
linhas = entrada.readlines() #Ler o restante do arquivo

imagem = np.array(list(linhas))
imagem = np.reshape(imagem, [dimensoes[1], dimensoes[0], 3])
imagem = imagem.astype(int)

#escrevendo a imagem cópia
saida.write("P2\n")
saida.write("#Criado por Gideone\n")
largura = dimensoes[0]
altura = dimensoes[1]
saida.write(str(largura))
saida.write(" ")
saida.write(str(altura))
saida.write("\n")
saida.write("255\n")

for i in range(len(imagem)):
    for j in range(len(imagem[1])):
        pixel = int((imagem[i][j][0] + imagem[i][j][1] + imagem[i][j][2]) / 3)
        saida.write(str(pixel))
        saida.write("\n")
        
#fechar os dois arquivos.
entrada.close()
saida.close()