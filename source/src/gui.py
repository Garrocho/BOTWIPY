# coding: utf-8

import sys
import settings
from PyQt4 import QtGui, QtCore, QtWebKit

class JanelaInicial(QtGui.QMainWindow):
    
    def __init__(self):
        super(JanelaInicial, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
    
        self.webView = QtWebKit.QWebView()
        
        self.html = open(settings.HTML).read()
        
        self.iniciarBot = QtGui.QAction(QtGui.QIcon(settings.INICIAR), 'Iniciar', self)
        self.iniciarBot.setShortcut('Ctrl+I')
        self.iniciarBot.setStatusTip('Iniciar o Bot - Ctrl+I')
        self.iniciarBot.triggered.connect(self.close)
        
        self.pararBot = QtGui.QAction(QtGui.QIcon(settings.PARAR), 'Parar', self)
        self.pararBot.setShortcut('Ctrl+P')
        self.pararBot.setStatusTip('Parar o Bot - Ctrl+P')
        self.pararBot.triggered.connect(self.close)
        
        self.confBot = QtGui.QAction(QtGui.QIcon(settings.CONFIGURAR), 'Configurar', self)
        self.confBot.setShortcut('Ctrl+C')
        self.confBot.setStatusTip('Configurar o Bot - Ctrl+C')
        self.confBot.triggered.connect(self.close)
        
        self.atuaBot = QtGui.QAction(QtGui.QIcon(settings.ATUALIZAR), 'Atualizar', self)
        self.atuaBot.setShortcut('Ctrl+A')
        self.atuaBot.setStatusTip('Atualizar Twitter - Ctrl+A')
        self.atuaBot.triggered.connect(self.close)
        
        self.keysBot = QtGui.QAction(QtGui.QIcon(settings.CHAVES), 'Chaves', self)
        self.keysBot.setShortcut('Ctrl+K')
        self.keysBot.setStatusTip('Chaves do Bot - Ctrl+K')
        self.keysBot.triggered.connect(self.close)
        
        self.ajuda = QtGui.QAction(QtGui.QIcon(settings.AJUDA), 'Ajuda', self)
        self.ajuda.setShortcut('Ctrl+H')
        self.ajuda.setStatusTip('Ajuda do Bot - Ctrl+H')
        self.ajuda.triggered.connect(self.chamarAjuda)
        
        self.sair = QtGui.QAction(QtGui.QIcon(settings.SAIR), 'Sair', self)
        self.sair.setShortcut('Ctrl+Q')
        self.sair.setStatusTip('Sair da Aplicacao - Ctrl+Q')
        self.sair.triggered.connect(self.close)

        self.toolBar = self.addToolBar('Sair')

    def adicionar(self):
        
        self.webView.setHtml(self.html)
        self.webView.page().mainFrame().evaluateJavaScript('createDiv("%s")' % ("<b>charles garrocho</b> (19 minutos atras)<br> Primeira Mensagem do bot... <a href='http://www.google.com'>ReTwittar</a>",))
        self.webView.page().mainFrame().evaluateJavaScript('createDiv("%s")' % ("<b>arthur assuncao</b> (23 minutos atras)<br> A Garantia do Twitter Nao e Boa... <a href='http://www.google.com'>ReTwittar</a>",))
        self.webView.page().mainFrame().evaluateJavaScript('createDiv("%s")' % ("<b>alemao</b> (28 minutos atras)<br> Temos Muito no Que Trabalhar... <a href='http://www.google.com'>ReTwittar</a>",))
        
        self.setCentralWidget(self.webView)

        self.toolBar.addAction(self.iniciarBot)
        self.toolBar.addAction(self.pararBot)
        self.toolBar.addAction(self.atuaBot)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.keysBot)
        self.toolBar.addAction(self.confBot)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.ajuda)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.sair)

    def configurar(self):
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setGeometry(600, 600, 650, 550)
        self.setWindowTitle('BOTWIPY - Bot em Python Para Twitter')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.statusBar().showMessage('O Bot Está Desligado...')
        self.show()
    
    def chamarAjuda(self):
        exAjuda = JanelaAjuda()
        exAjuda.exec_()


class JanelaAjuda(QtGui.QDialog):
    
    def __init__(self):
        super(JanelaAjuda, self).__init__()
        self.iniciar()
        self.configurar()
        
    def iniciar(self):
        pass
        self.labelImagem = QtGui.QLabel(QtGui.QIcon(settings.LOGO))
        self.setCentralWidget(self.labelImagem)

    def configurar(self):
        self.setGeometry(300, 300, 350, 250)
        self.setModal(True)
        self.setWindowTitle('Ajuda - Bot em Python Para Twitter')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        self.center()
        self.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = JanelaInicial()
    sys.exit(app.exec_())
