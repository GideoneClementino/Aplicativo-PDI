# -*- coding: utf:8 -*-
import sys
import numpy as np
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *


class Binaria(QWidget):
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
        self.setWindowTitle('Transformação Binária')
        self.show()

    def adiciona_valor(self):
        num, ok = QInputDialog.getDouble(self, "Filtro Gama", "Valor")
        if ok:
            self.threshold_edit.setText(str(num))

    def confirma_threshold(self):
        #Abrir os arquivos de entrada e de saída
        entrada = open(sys.argv[1], "r+")
        saida = open(sys.argv[2], "w+")

        linha = entrada.readline()  # P3
        linha = entrada.readline()  # Comentário
        linha = entrada.readline()  # Dimensões
        dimensoes = linha.split()
        largura = int(dimensoes[0])
        altura = int(dimensoes[1])
        linha = entrada.readline()  # Valor fixo
        linha = entrada.readlines()  # Ler o restante do arquivo e grava como lista

        # converter de lista para array
        imagem = np.asarray(linha, dtype=float)
        # reshape
        imagem = np.reshape(imagem, (altura, largura))

        # escrevendo a imagem cópia
        saida.write("P1\n")
        saida.write("#Criado por Gideone\n")
        saida.write(str(largura))
        saida.write(" ")
        saida.write(str(altura))
        saida.write("\n")

        #Recebendo valor digitado pelo usuario
        valor = self.threshold_edit.text()
        valor = float(valor)
        # fazer a cópia
        for i in range(len(imagem)):
            for j in range(len(imagem[1])):
                if imagem[i][j] > valor:
                    saida.write("0")
                else:
                    saida.write("1")
                saida.write("\n")
        # fechar os dois arquivos.
        entrada.close()
        saida.close()
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = Binaria()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
