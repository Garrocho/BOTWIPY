#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
    
        tableWidget = TableWidget(4, 3)
        tableWidget.addLinha(["Charles Garrocho", "Ola amgigos", "10:50:35"])
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
        """Center the window on the screen."""
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
  
class TableWidget(QtGui.QTableWidget):
    qtde_linhas = 0

    def __init_(self, linhas, colunas):
        self.super.__init__(linhas, colunas)
        
    def addLinha(self, dados):
        cont = 0
        for dado in dados:
            item = QtGui.QTableWidgetItem(dado)
            self.setItem(self.qtde_linhas, cont, item)
            cont = cont + 1
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

