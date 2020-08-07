# -*- coding: utf:8 -*-
import sys
import subprocess
import os
import numpy as np
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QGridLayout, QWidget, QMessageBox, QFileDialog, QProgressBar
from PyQt5.QtCore import *

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setup_main_window()
        self.initUI() 

    def setup_main_window(self):
        self.x = 640
        self.y = 480
        self.setMinimumSize(QSize(self.x, self.y))
        self.setWindowTitle("PDI - Processamento Digital de Imagens")
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.layout = QGridLayout()
        self.wid.setLayout(self.layout)

    def initUI(self):
        #Criar a barra de menu
        self.barrademenu = self.menuBar()

        #Criar os menus
        self.menuarquivo = self.barrademenu.addMenu("&Arquivo")
        self.menutransformacoes = self.barrademenu.addMenu("&Transformações")
        self.menufiltros = self.barrademenu.addMenu("&Filtros")
        self.menudeteccao = self.barrademenu.addMenu("&Detecção de Bordas")
        self.menusobre = self.barrademenu.addMenu("&Sobre")

        self.opcaoabrir = self.menuarquivo.addAction("&Abrir")
        self.opcaoabrir.triggered.connect(self.open_file)
        self.opcaoabrir.setShortcut("Ctrl+A")
        self.opcaoabrir.setCheckable(True)
        self.opcaoabrir.setChecked(False)

        self.save_as = self.menuarquivo.addAction("&Salvar Como...")
        self.save_as.setShortcut("Ctrl+S")
        self.save_as.triggered.connect(self.salvar_como)

        self.menuarquivo.addSeparator()

        self.opcaofechar = self.menuarquivo.addAction("F&echar")
        self.opcaofechar.setShortcut("Ctrl+X")
        self.opcaofechar.triggered.connect(self.close)

        self.opcaosobre = self.menusobre.addAction("Sobre")
        self.opcaosobre.triggered.connect(self.exibe_mensagem)

        self.opcao_imagem = self.menusobre.addAction("Informações da Imagem")
        self.opcao_imagem.triggered.connect(self.exibe_informacao_imagem)

        self.opcaoapagar = self.menusobre.addAction("Apagar")
        self.opcaoapagar.triggered.connect(self.apagar_mensagem)

        #Menu de Transformações
        self.trans_morfo = self.menutransformacoes.addMenu("Transformações Morfológicas")

        self.erosao = self.trans_morfo.addAction("Erosão")
        self.erosao.triggered.connect(self.transform_erosao)

        self.dilatacao = self.trans_morfo.addAction("Dilatação")
        self.dilatacao.triggered.connect(self.transform_dilatacao)

        self.abertura = self.trans_morfo.addAction("Abertura")
        self.abertura.triggered.connect(self.transform_abertura)

        self.fechamento = self.trans_morfo.addAction("Fechamento")
        self.fechamento.triggered.connect(self.transform_fechamento)

        self.opcao_pgm = self.menutransformacoes.addAction("Colorida para escala de cinza")
        self.opcao_pgm.triggered.connect(self.transform_cinza)

        self.opcao_bin = self.menutransformacoes.addAction("Para preto e branco")
        self.opcao_bin.triggered.connect(self.para_binaria)

        self.separacao_rgb = self.menutransformacoes.addAction("Separação RGB")
        self.separacao_rgb.triggered.connect(self.transform_escala_rgb)

        self.opcaonegativo = self.menutransformacoes.addAction("Negativo")
        self.opcaonegativo.triggered.connect(self.transform_negativo)

        self.opcaogama = self.menutransformacoes.addAction("Correção Gamma")
        self.opcaogama.triggered.connect(self.transform_filtro_gama)
        
        #Menu de Filtros
        self.opcaogauss = self.menufiltros.addAction("Filtro Gaussiano")
        self.opcaogauss.triggered.connect(self.transform_gauss)        

        self.opcaosharpen = self.menufiltros.addAction("Filtro Sharpen")
        self.opcaosharpen.triggered.connect(self.transform_sharpen)

        self.opcaologaritmo = self.menufiltros.addAction("Filtro Logaritmo")
        self.opcaologaritmo.triggered.connect(self.transform_filtro_logaritmo)

        self.opcaomediana = self.menufiltros.addAction("Filtro Mediana(box blur)")
        self.opcaomediana.triggered.connect(self.transform_filtro_mediana)

        #Menu de Detecção de Bordas
        self.opcao_sobel = self.menudeteccao.addAction("Filtro Sobel")
        self.opcao_sobel.triggered.connect(self.transform_sobel)

        self.edge = self.menudeteccao.addAction("Três Filtros")
        self.edge.triggered.connect(self.transform_edge_detection)

        self.detec_erosao = self.menudeteccao.addAction("Erosão")
        self.detec_erosao.triggered.connect(self.deteccao_erosao)
        
        self.detec_dilatacao = self.menudeteccao.addAction("Dilatação")
        self.detec_dilatacao.triggered.connect(self.deteccao_dilatacao)

        #Criar barra de status
        self.barradestatus = self.statusBar()
        self.barradestatus.showMessage("Oi, bem-vindo ao meu software!", 3000)

        #Criando QLabel para texto
        self.texto = QLabel("Conversão de filtros", self)
        self.texto.adjustSize()
        self.largura = self.texto.frameGeometry().width()
        self.altura = self.texto.frameGeometry().height()
        self.texto.setAlignment(QtCore.Qt.AlignCenter)    

        #Criando as imagems (QLbabel)
        self.imagem1 = QLabel(self)
        self.endereco1 = 'images/watchmen.ppm'
        self.pixmap1 = QtGui.QPixmap(self.endereco1)
        self.pixmap1 = self.pixmap1.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
        self.imagem1.setPixmap(self.pixmap1)
        self.imagem1.setAlignment(QtCore.Qt.AlignCenter)  
        
        self.imagem2 = QLabel(self)
        self.endereco2 = 'images/watchmen.ppm'
        self.pixmap2 = QtGui.QPixmap(self.endereco2)
        self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
        self.imagem2.setPixmap(self.pixmap2)
        self.imagem2.setAlignment(QtCore.Qt.AlignCenter) 

        #Organizando os widgets dentro da GridLayout
        self.layout.addWidget(self.texto, 0, 0, 1, 2) 
        self.layout.addWidget(self.imagem1, 1, 0)
        self.layout.addWidget(self.imagem2, 1, 1)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 0)

    #Metodos para ação dos botões
    def apagar_mensagem(self):
        self.barradestatus.clearMessage()

    def exibe_mensagem(self):
        #self.barradestatus.showMessage("Você clicou na Sobre")
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Gideone Clementino da Silva")
        self.msg.setWindowTitle("Sobre")
        self.msg.setInformativeText("Santa Vitoria - MG | 29 de Junho de 2020")
        self.msg.setDetailedText("Aplicativo para transformações Gaussiana, sharpen e sobel")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.exec_()
        self.reply = self.msg.clickedButton()
        self.barradestatus.showMessage("Foi clicado o botão: " + self.reply.text())
        
        if self.reply.text() == "OK":
            print("Apertou OK")
        if self.reply.text() == "Cancel":
            print("Apertou Cancel")

    def exibe_informacao_imagem(self):             
        self.entrada = open(self.endereco1, "r+")
        self.linha1 = self.entrada.readline() 
        self.linha2 = self.entrada.readline() 
        self.linha3 = self.entrada.readline() 
        self.dimensoes = self.linha3.split()
        self.largura = self.dimensoes[0]
        self.altura = self.dimensoes[1]
        self.string = self.endereco1
        self.particao1 = self.string.rpartition('/')
        self.particao2 = self.string.rpartition('.')

        self.msg2 = QMessageBox()
        self.msg2.setIcon(QMessageBox.Information)
        self.msg2.setText("Nome: " + self.particao1[2] + "\n" + "Extensão do Arquivo: " + self.particao2[2] + "\n" + "Largura : " +  self.largura + "\n" + "Altura: " +  self.altura)
        self.msg2.setWindowTitle("Informações da Imagem")
        self.msg2.setDetailedText(self.linha2)

        self.msg2.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg2.exec_()
        self.reply = self.msg2.clickedButton()
        self.barradestatus.showMessage("Foi clicado o botao: " + self.reply.text())

    def open_file(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Open image', directory=QtCore.QDir.currentPath(), filter='All files (*.*);;Images (*.ppm; *.pgm;*.pbm)', initialFilter='Images (*.ppm; *.pgm;*.pbm)')
        print(fileName)
        if fileName != '':
            self.endereco1 = fileName
            self.pixmap1 = QtGui.QPixmap(self.endereco1)
            self.pixmap1 = self.pixmap1.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem1.setPixmap(self.pixmap1)
            self.e_dando_dicas()
    
    def salvar_como(self):
        options = QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Save image', directory=QtCore.QDir.currentPath(), filter='All files (*.*);;Images (*.ppm; *.pgm;*.pbm)', initialFilter= 'Images (*.ppm; *.pgm;*.pbm)', options=options)
        if fileName != '':
            string = self.endereco2                
            self.particao = string.rpartition('.')                    
            try:               
                shutil.copyfile(self.endereco2, fileName)    
                self.arquivo_salvo()
            except shutil.SameFileError:
                print("Arquivo de origem e destino sao iguais")
            except IsADirectoryError:
                print("O destino é um diretorio")
            except PermissionError:
                print("Permissão negada")
            except:
                print("Erro ao salvar arquivo")
    def e_dando_dicas(self):
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):
            self.status = self.statusBar()
            self.status.showMessage("Você abriu uma imagem em escala de cinza", 15000)            
        elif (self.particao[2] == 'ppm'):
            self.status = self.statusBar()
            self.status.showMessage("Você abriu uma imagem colorida", 15000)   
        elif (self.particao[2] == 'pbm'):
            self.status = self.statusBar()
            self.status.showMessage("Você abriu uma imagem binária", 15000)    

    def transform_sobel(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')        
        self.entrada = self.endereco1
        if (self.particao[2] == 'pgm'):                
            self.saida = 'images/sobel_novo.pgm'
            self.script = '.\scripts\sobel.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/sobel_novo.ppm'
            self.script = '.\scripts\sobel.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)   
        else:
            self.erro_message()         

    def transform_gauss(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')        
        self.entrada = self.endereco1
        if (self.particao[2] == 'pgm'):        
            self.saida = 'images/gauss_novo.pgm'
            self.script = '.\scripts\para_gaussiana.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)                        
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/gauss_novo.ppm'  
            self.script = '.\scripts\para_gaussiana.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)             
        else:
            self.erro_message()                           

    def transform_sharpen(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):         
            self.saida = 'images/sharpen_novo.pgm'
            self.script = '.\scripts\sharpen.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/negativo_novo.ppm'
            self.saida = 'images/sharpen_novo.pgm'
            self.script = '.\scripts\sharpen.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)            
        else:
            self.erro_message()                

    def transform_negativo(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):                
            self.saida = 'images/negativo_novo.pgm'
            self.script = '.\scripts\para_negativo.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)            
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/negativo_novo.ppm'
            self.script = '.\scripts\para_negativo.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)                
        else:
            self.erro_message()            

    def transform_filtro_gama(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):
            self.saida = 'images/filtro_gama_novo.pgm'
            self.script = '.\scripts\para_gama.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/filtro_gama_novo.ppm'    
            self.saida = 'images/filtro_gama_novo.pgm'
            self.script = '.\scripts\para_gama.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)                    
        else:
            self.erro_message()

    def transform_filtro_logaritmo(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):
            self.saida = 'images/filtro_logaritmo_novo.pgm'
            self.script = '.\scripts\para_logaritma.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)            
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/filtro_logaritmo_novo.ppm' 
            self.script = '.\scripts\para_logaritma.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)                     
        else:
            self.erro_message()                      

    def transform_filtro_mediana(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):
            self.saida = 'images/filtro_mediana_novo.pgm'   
            self.script = '.\scripts\para_mediana.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)               
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/filtro_mediana_novo.ppm'
            self.script = '.\scripts\para_mediana.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.erro_message()

    def transform_cinza(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')        
        if (self.particao[2] == 'ppm'):
            self.saida = 'images/para_pgm_novo.pgm'   
            self.script = '.\scripts\para_cinza.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)      
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens coloridas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()       

    def para_binaria(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):
            self.saida = 'images/para_binaria_novo.pbm'
            self.script = '.\scripts\para_binaria.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Primeiro converta para escala de cinza")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()        

    def transform_edge_detection(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pgm'):
            self.saida = 'images/tres_filtros_novo.pgm'
            self.script = '.\scripts\edge_detection.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        elif (self.particao[2] == 'ppm'):
            self.saida = 'images/tres_filtros_novo.ppm'
            self.script = '.\scripts\edge_detection.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.erro_message()

    def transform_escala_rgb(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'ppm'):
            self.saida = 'images/separacao_rgb.ppm'
            self.script = '.\scripts\para_r_g_b.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens coloridas são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()    

    def transform_erosao(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pbm'):
            self.saida = 'images/erosao.pbm'
            self.script = '.\scripts\m_erosao.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens binárias são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()        
     
    def transform_dilatacao(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pbm'):
            self.saida = 'images/dilatacao.pbm'
            self.script = '.\scripts\m_dilatacao.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens binárias são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()   

    def transform_abertura(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pbm'):
            self.saida = 'images/abertura.pbm'
            self.script = '.\scripts\m_abertura.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens binárias são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()   

    def transform_fechamento(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pbm'):
            self.saida = 'images/fechamento.pbm'
            self.script = '.\scripts\m_fechamento.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens binárias são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()
    
    def deteccao_erosao(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pbm'):
            self.saida = 'images/deteccao_erosao.pbm'
            self.script = '.\scripts\d_erosao.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens binárias são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()
        
    def deteccao_dilatacao(self):
        self.entrada = self.endereco1
        string = self.endereco1
        self.particao = string.rpartition('.')
        if (self.particao[2] == 'pbm'):
            self.saida = 'images/deteccao_dilatacao.pbm'
            self.script = '.\scripts\d_dilatacao.py'
            self.program = 'python ' + self.script + ' ' + self.entrada + ' '  + self.saida
            print(self.program)
            subprocess.run(self.program, shell=True)
            self.endereco2 = self.saida
            self.pixmap2 = QtGui.QPixmap(self.endereco2)
            self.pixmap2 = self.pixmap2.scaled(260, 287, QtCore.Qt.KeepAspectRatio)
            self.imagem2.setPixmap(self.pixmap2)
        else:
            self.error = QMessageBox()
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("ERRO")
            self.error.setText("Apenas imagens binárias são aceitas")
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.exec_()

    def erro_message(self):
        self.error = QMessageBox()
        self.error.setIcon(QMessageBox.Warning)
        self.error.setWindowTitle("ERRO")
        self.error.setText("Apenas arquivos PGM OU PPM")
        self.error.setStandardButtons(QMessageBox.Ok)
        self.error.exec_() 

    def arquivo_salvo(self):
        self.save = QMessageBox()
        self.save.setIcon(QMessageBox.Information)
        self.save.setWindowTitle("Sucesso")
        self.save.setText("Aquivo salvo com sucesso")
        self.save.setStandardButtons(QMessageBox.Ok)
        self.save.exec_() 

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
window()
