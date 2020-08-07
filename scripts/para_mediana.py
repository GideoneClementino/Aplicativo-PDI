# -*- coding: utf:8 -*-
import sys
import numpy as np
import math

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

#Mediana
kernel = np.ones((3,3))
kernel = np.asarray(kernel)/9
ks = int((len(kernel)-1)/2)

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
                    sum = sum + (imagem[i - ks + ki][j - ks + kj]*kernel[ki][kj])
            sum = int(sum)
            sum = str(sum)
            saida.write(sum)
            saida.write("\n")
            
elif (particao1[2] == 'ppm'):
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

#fechar os dois arquivos.
entrada.close()
saida.close()
