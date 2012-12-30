#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
    
        tableWidget = TableWidget(3, 3)
        tableWidget.configura()
        tableWidget.addLinha(["Charles Garrocho", "Ola amigos", "10:50:35"])
        tableWidget.addLinha(["Thiago Garrocho", "Noob kitter", "10:52:59"])
        tableWidget.addLinha(["Gustavo Garrocho", "Caramba em so tem kiter...", "10:53:38"])
        self.setCentralWidget(tableWidget)

        self.iniciarBot = QtGui.QAction(QtGui.QIcon('./icons/start24.png'), 'Iniciar', self)
        self.iniciarBot.setShortcut('Ctrl+I')
        self.iniciarBot.setStatusTip('Iniciar o Bot - Ctrl+I')
        self.iniciarBot.triggered.connect(self.close)
        
        self.pararBot = QtGui.QAction(QtGui.QIcon('./icons/end24.png'), 'Parar', self)
        self.pararBot.setShortcut('Ctrl+P')
        self.pararBot.setStatusTip('Parar o Bot - Ctrl+P')
        self.pararBot.triggered.connect(self.close)
        
        self.confBot = QtGui.QAction(QtGui.QIcon('./icons/edit24.png'), 'Configurar', self)
        self.confBot.setShortcut('Ctrl+C')
        self.confBot.setStatusTip('Configurar o Bot - Ctrl+C')
        self.confBot.triggered.connect(self.close)
        
        self.ajuda = QtGui.QAction(QtGui.QIcon('./icons/help24.png'), 'Ajuda', self)
        self.ajuda.setShortcut('Ctrl+H')
        self.ajuda.setStatusTip('Ajuda do Bot - Ctrl+H')
        self.ajuda.triggered.connect(self.close)
        
        self.sair = QtGui.QAction(QtGui.QIcon('./icons/exit24.png'), 'Sair', self)
        self.sair.setShortcut('Ctrl+Q')
        self.sair.setStatusTip('Sair da Aplicacao - Ctrl+Q')
        self.sair.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Arquivo')
        fileMenu.addAction(self.sair)

        toolBar = self.addToolBar('Sair')
        toolBar.setMovable(False)
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        toolBar.addAction(self.iniciarBot)
        toolBar.addAction(self.pararBot)
        toolBar.addAction(self.confBot)
        toolBar.addSeparator()
        toolBar.addAction(self.ajuda)
        toolBar.addSeparator()
        toolBar.addAction(self.sair)
        
        self.setGeometry(600, 600, 650, 550)
        self.setWindowTitle('BOTWIPY - Bot em Python Para Twitter')
        self.setWindowIcon(QtGui.QIcon('./icons/twitter.png'))
        self.center()
        self.show()
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
  
class TableWidget(QtGui.QTableWidget):
    qtde_linhas = 0

    def __init_(self, linhas, colunas):
        self.super.__init__(linhas, colunas)
    
    def configura(self):
        self.setHorizontalHeaderLabels(['Usuario', 'Mensagem','Horario'])
        self.itemDoubleClicked.connect(self.editItem)
        self.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.setSortingEnabled(False)
        self.setColumnWidth(0, 130)
        self.setColumnWidth(1, 430)
        self.setColumnWidth(2, 70)
        
    def addLinha(self, dados):
        cont = 0
        for dado in dados:
            item = QtGui.QTableWidgetItem(dado)
            self.setItem(self.qtde_linhas, cont, item)
            cont += 1
        self.qtde_linhas += 1
        
    def editItem(self,clicked):
        print clicked.row()
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

