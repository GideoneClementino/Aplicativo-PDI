# -*- coding: utf:8 -*-
import sys
import numpy as np
import math

#Checando os argumentos de linha de comando
if __name__ == "__main__":
    print(f'Quantos argumentos: {len(sys.argv)}')
    for i, arg in enumerate(sys.argv):
        print(f"Argument: {i}: {arg}")

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
particao1 = string.rpartition('.')

if (particao1[2] == 'pgm'):
    #escrevendo a imagem cópia
    saida.write("P2\n")
    saida.write("#Criado por Gideone\n")
    saida.write(largura)
    saida.write(" ")
    saida.write(altura)
    saida.write("\n")
    saida.write("255\n")
elif (particao1[2] == 'ppm'):
    #escrevendo a imagem cópia
    saida.write("P3\n")
    saida.write("#Criado por Gideone\n")
    saida.write(largura)
    saida.write(" ")
    saida.write(altura)
    saida.write("\n")
    saida.write("255\n")    

for i in range((len(imagem))):
    n = int((math.log(1 + (imagem[i]/255)))*255)
    n = str(n)
    saida.write(n) 
    saida.write("\n")

#fechar os dois arquivos
entrada.close()
saida.close()
