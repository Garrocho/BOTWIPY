#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

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

        exitAction = QtGui.QAction(QtGui.QIcon('./icons/exit24.png'), 'Sair', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Sair da Aplicacao')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Arquivo')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Sair')
        toolbar.addAction(exitAction)
        
        self.setGeometry(600, 600, 650, 550)
        self.setWindowTitle('BOTWIPY - Bot em Python Para Twitter')
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
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

