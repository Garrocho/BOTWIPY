# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import re
import sys
import time
import settings
import botwipy
from threading import Thread
from PyQt4 import QtGui, QtCore, QtWebKit, Qt

# Conectando a API utilizando os dados da aplicação.
global bot
bot = botwipy.BotAPI()


class IniciarBot(QtCore.QThread):
    mensagem_lista = QtCore.pyqtSignal(str)
    mensagem_status_bar = QtCore.pyqtSignal(str)

    def run(self):

        if bot.get_meu_nome() != None:
            while bot.RODAR:

                if bot.MSG_SEG == True:
                    self.mensagem_status_bar.emit('Obtendo Lista de Mensagens dos Meus Seguidores')
                    amigos_tweets = bot.get_amigos_tweets()
                    for tweet in amigos_tweets:
                        self.mensagem_status_bar.emit(tweet.text)
                        usuario = bot.verifica_tweet(tweet, 'RT @(.*?):')
                        if usuario is not None:
                            seguir = bot.seguir_usuario(usuario[0])
                            print seguir
                            self.mensagem_lista.emit('<b>{0}</b><i> <font>{1}</font> </i> <br>{2}'.format(bot.get_meu_nome(), usuario[1], seguir))

                if bot.MENSOES == True:
                    self.mensagem_status_bar.emit('Obtendo Lista de Minhas Mensoes')
                    for usuario in bot.get_mensoes():
                        self.mensagem_lista.emit('<b>{0}</b> <br> {1}'.format(bot.get_meu_nome(), bot.seguir_usuario(usuario[1])))
                        novo_status = u'Ola @{0}. Obrigado pela sua mensagem! :-)'.format(usuario[1])
                        self.mensagem_lista.emit('<b>{0}</b> <br> Atualizou seu Status para: {1}'.format(bot.get_meu_nome(), novo_status))
                        bot.atualizar_status(novo_status)
                time.sleep(bot.INTERVALO)
        else:
            self.mensagem_status_bar.emit('ERRO')


class PararBot(QtCore.QThread):
    mensagem_status_bar = QtCore.pyqtSignal(str)
    
    def run(self):
        bot.RODAR = False
        self.mensagem_status_bar.emit('Parando o BoTWiPy')


class JanelaInicial(QtGui.QMainWindow):
    """
    Essa é a Interface gráfica inicial do botwipy. Nela é definido uma barra de
    botões o carregamento de uma lista de um arquivo html e a barra de status.
    """

    def __init__(self):
        super(JanelaInicial, self).__init__()
        self.iniciar()
        self.adicionar()
        self.pIniciar = IniciarBot()
        self.pIniciar.mensagem_lista.connect(self.recebe_msg_init_lista)
        self.pIniciar.mensagem_status_bar.connect(self.recebe_msg_init_status)
        self.pParar = PararBot()
        self.pParar.mensagem_status_bar.connect(self.recebe_msg_init_status)

        if bot.INIT == True:
            self.iniciar_bot()
        else:
            self.parar_bot()

        self.configurar()
   
    def recebe_msg_init_lista(self, mensagem):
        self.webView.page().mainFrame().evaluateJavaScript('novoElemento("%s")' % (mensagem,))

    def recebe_msg_init_status(self, mensagem):
        if mensagem == 'ERRO':
            QtGui.QMessageBox.about(self, "Erro", "Impossivel Iniciar o BoTWiPy\nChaves Incorretas")
        else:
            self.statusBar().showMessage(mensagem)

    def iniciar(self):
    
        self.webView = QtWebKit.QWebView()
        
        self.html = open(settings.HTML).read()
        
        self.iniciarBot = QtGui.QAction(QtGui.QIcon(settings.INICIAR), 'Iniciar', self)
        self.iniciarBot.setShortcut('Ctrl+I')
        self.iniciarBot.setStatusTip('Iniciar o Bot - Ctrl+I')
        self.iniciarBot.triggered.connect(self.iniciar_bot)
        
        self.pararBot = QtGui.QAction(QtGui.QIcon(settings.PARAR), 'Parar', self)
        self.pararBot.setShortcut('Ctrl+S')
        self.pararBot.setStatusTip('Parar o Bot - Ctrl+S')
        self.pararBot.triggered.connect(self.parar_bot)
        
        self.confBot = QtGui.QAction(QtGui.QIcon(settings.CONFIGURAR), 'Preferencias', self)
        self.confBot.setShortcut('Ctrl+P')
        self.confBot.setStatusTip('Preferencias do Bot - Ctrl+P')
        self.confBot.triggered.connect(self.chamar_preferencias)
        
        self.atuaBot = QtGui.QAction(QtGui.QIcon(settings.LIMPAR), 'Limpar', self)
        self.atuaBot.setShortcut('Ctrl+A')
        self.atuaBot.setStatusTip('Atualizar Twitter - Ctrl+A')
        self.atuaBot.triggered.connect(self.limpar_lista)
        
        self.keysBot = QtGui.QAction(QtGui.QIcon(settings.CHAVES), 'Chaves', self)
        self.keysBot.setShortcut('Ctrl+C')
        self.keysBot.setStatusTip('Chaves do Bot - Ctrl+C')
        self.keysBot.triggered.connect(self.chamar_chaves)
        
        self.sobre = QtGui.QAction(QtGui.QIcon(settings.AJUDA), 'Sobre', self)
        self.sobre.setShortcut('Ctrl+H')
        self.sobre.setStatusTip('Sobre o BotWiPy - Ctrl+H')
        self.sobre.triggered.connect(self.chamar_sobre)
        
        self.sair = QtGui.QAction(QtGui.QIcon(settings.SAIR), 'Sair', self)
        self.sair.setShortcut('Ctrl+Q')
        self.sair.setStatusTip('Sair da Aplicacao - Ctrl+Q')
        self.sair.triggered.connect(self.close)

        self.toolBar = self.addToolBar('Sair')
        self.statusBar()

    def adicionar(self):
        
        self.webView.setHtml(self.html)
        self.setCentralWidget(self.webView)
        
        self.toolBar.addAction(self.iniciarBot)
        self.toolBar.addAction(self.pararBot)
        self.toolBar.addAction(self.atuaBot)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.keysBot)
        self.toolBar.addAction(self.confBot)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.sobre)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.sair)

    def configurar(self):
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setFixedSize(670, 600)
        self.setWindowTitle('BOTWIPY - Bot em Python Para Twitter')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.show()
    
    def iniciar_bot(self):
        bot.RODAR = True
        self.pIniciar.start()

    def parar_bot(self):
        self.pParar.start()
    
    def limpar_lista(self):
        self.webView.page().mainFrame().evaluateJavaScript('LimparLista()')
    
    def chamar_sobre(self):
        exSobre = DialogoSobre()
        exSobre.exec_()

    def chamar_chaves(self):
        exChaves = DialogoChaves()
        exChaves.exec_()

    def chamar_preferencias(self):
        exPreferencias = DialogoPreferencias()
        exPreferencias.exec_()


class DialogoSobre(QtGui.QDialog):
    """
    Essa é a Interface gráfica do dialogo sobre, onde contém as informações de
    software. Nela é definido vários rótulos e uma imagem logo do software.
    """
    
    def __init__(self):
        super(DialogoSobre, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
        self.vbox = QtGui.QHBoxLayout()                                        
        self.setLayout(self.vbox)
          
        self.foto_label = QtGui.QLabel()
        self.foto_label.setPixmap(QtGui.QPixmap(settings.LOGO))
        self.label = QtGui.QLabel('<H3>Informacoes do software</H3> <b>Software: </b>Bot Twitter em Python <br> <b>Versao: </b> 1.0 <br> <b>Copyright: </b>Open Source<br> <H3>Desenvolvedores</H3> Charles Tim Batista Garrocho <br>Paulo Vitor Francisco')
        
    def adicionar(self):
        self.vbox.addWidget(self.foto_label)
        self.vbox.addWidget(self.label)

    def configurar(self):
        self.setModal(True)
        self.setWindowTitle('BoTWiPy - Sobre o Software')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        self.setFixedSize(410, 215)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)
        self.show()


class DialogoChaves(QtGui.QDialog):
    """
    Essa é a Interface gráfica do dialogo de definição de chaves para o acesso
    a conta twitter. Nela é definido vários rótulos e campos de texto e botões.
    """
    
    def __init__(self):
        super(DialogoChaves, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
        self.boxTotal = QtGui.QVBoxLayout()
        self.boxRotuloCampo = QtGui.QHBoxLayout()
        self.boxRotulo = QtGui.QVBoxLayout()
        self.boxCampo = QtGui.QVBoxLayout()
        self.boxBotao = QtGui.QHBoxLayout()
        
        self.botaoGravar = QtGui.QPushButton(QtGui.QIcon(settings.GRAVAR), 'Gravar')
        self.botaoGravar.setIconSize(QtCore.QSize(30,30));
        self.botaoGravar.clicked.connect(self.gravar)
        
        self.botaoCancelar = QtGui.QPushButton(QtGui.QIcon(settings.CANCELAR), 'Cancelar')
        self.botaoCancelar.setIconSize(QtCore.QSize(30,30));
        self.botaoCancelar.clicked.connect(self.close)
        
        self.botaoLimpar = QtGui.QPushButton(QtGui.QIcon(settings.LIMPAR), 'Limpar')
        self.botaoLimpar.setIconSize(QtCore.QSize(30,30));
        self.botaoLimpar.clicked.connect(self.limpar)
        
        self.rotuloConsumerKey = QtGui.QLabel('Consumer Key')
        self.campoTextoConsumerKey = QtGui.QLineEdit(bot.redis.get('CONSUMER_KEY'))
        
        self.rotuloConsumerSecret = QtGui.QLabel('Consumer Secret')
        self.campoTextoConsumerSecret = QtGui.QLineEdit(bot.redis.get('CONSUMER_SECRET'))

        self.rotuloAcessToken = QtGui.QLabel('Acess Token')
        self.campoTextoAcessToken = QtGui.QLineEdit(bot.redis.get('OAUTH_TOKEN'))
        
        self.rotuloAcessTokenSecret = QtGui.QLabel('Acess Token Secret')
        self.campoTextoAcessTokenSecret = QtGui.QLineEdit(bot.redis.get('OAUTH_TOKEN_SECRET'))

    def adicionar(self):
        self.boxTotal.addWidget(QtGui.QLabel('<b>Defina</b> abaixo as chaves de seguranca da <b>conta Twitter</b>'))
        self.boxRotulo.addWidget(self.rotuloConsumerKey)
        self.boxCampo.addWidget(self.campoTextoConsumerKey)

        self.boxRotulo.addWidget(self.rotuloConsumerSecret)
        self.boxCampo.addWidget(self.campoTextoConsumerSecret)

        self.boxRotulo.addWidget(self.rotuloAcessToken)
        self.boxCampo.addWidget(self.campoTextoAcessToken)

        self.boxRotulo.addWidget(self.rotuloAcessTokenSecret)
        self.boxCampo.addWidget(self.campoTextoAcessTokenSecret)

        self.boxBotao.addWidget(self.botaoGravar)
        self.boxBotao.addWidget(self.botaoLimpar)
        self.boxBotao.addWidget(self.botaoCancelar)

        self.boxRotuloCampo.addLayout(self.boxRotulo)
        self.boxRotuloCampo.addLayout(self.boxCampo)

        self.boxTotal.addLayout(self.boxRotuloCampo)
        self.boxTotal.addLayout(self.boxBotao)
        self.setLayout(self.boxTotal)

    def configurar(self):
        self.setModal(True)
        self.setWindowTitle('BoTWiPy - Chaves de Seguranca')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        self.setFixedSize(400, 240)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)
        self.show()

    def gravar(self):
        c_k = str(self.campoTextoConsumerKey.text())
        c_s_k = str(self.campoTextoConsumerSecret.text())
        o_t = str(self.campoTextoAcessToken.text())
        o_t_s = str(self.campoTextoAcessTokenSecret.text())

        if len(c_k) != 0 and len(c_s_k) != 0 and len(o_t) != 0 and len(o_t_s) != 0:

            a = open(settings.NOME).read()
            a = re.sub(settings.CONSUMER_KEY, c_k, a)
            a = re.sub(settings.CONSUMER_SECRET, c_s_k, a)
            a = re.sub(settings.OAUTH_TOKEN, o_t, a)
            a = re.sub(settings.OAUTH_TOKEN_SECRET, o_t_s, a)
            arq = open(settings.NOME, 'w')
            arq.write(a)
            arq.close()

            bot.redis.set('CONSUMER_KEY', c_k)
            bot.redis.set('CONSUMER_SECRET', c_s_k)
            bot.redis.set('OAUTH_TOKEN', o_t)
            bot.redis.set('OAUTH_TOKEN_SECRET', o_t_s)

            if bot.carrega_api() == True:
                QtGui.QMessageBox.about(self, "Sucesso", "Chaves Configuradas")
                self.close()
            else:

                QtGui.QMessageBox.about(self, "Atencao", "Dados Informados Incorretos")
        else:
            QtGui.QMessageBox.about(self, "Atencao", "Dados Incompletos")

    def limpar(self):
        self.campoTextoConsumerKey.setText('')
        self.campoTextoConsumerSecret.setText('')
        self.campoTextoAcessToken.setText('')
        self.campoTextoAcessTokenSecret.setText('')


class DialogoPreferencias(QtGui.QDialog):
    """
    Essa é a Interface gráfica do dialogo de preferências da api do bot.
    Nela é definido várias checagens de preferências.
    """
    
    def __init__(self):
        super(DialogoPreferencias, self).__init__()
        self.iniciar()
        self.adicionar()
        self.sld.setValue(bot.INTERVALO)
        self.configurar()
        
    def iniciar(self):
        self.boxTotal = QtGui.QVBoxLayout()
        self.boxCheckBox = QtGui.QVBoxLayout()
        self.boxIntervalo = QtGui.QHBoxLayout()
        self.boxBotao = QtGui.QHBoxLayout()

        self.checkBoxRoda = QtGui.QCheckBox('Iniciar BoTWiPy ao executar', self)
        if bot.INIT == True:
            self.checkBoxRoda.toggle()

        self.checkBoxMensoes = QtGui.QCheckBox('Analizar Mensoes ao BoTWiPy', self)
        if bot.MENSOES == True:
            self.checkBoxMensoes.toggle()

        self.checkBoxMsgSeg = QtGui.QCheckBox('Analizar Mensagens Followers', self)
        if bot.MSG_SEG == True:
            self.checkBoxMsgSeg.toggle()

        self.botaoGravar = QtGui.QPushButton(QtGui.QIcon(settings.GRAVAR), 'Gravar')
        self.botaoGravar.setIconSize(QtCore.QSize(30,30));
        self.botaoGravar.clicked.connect(self.gravar)
        
        self.botaoCancelar = QtGui.QPushButton(QtGui.QIcon(settings.CANCELAR), 'Cancelar')
        self.botaoCancelar.setIconSize(QtCore.QSize(30,30));
        self.botaoCancelar.clicked.connect(self.close)

    def adicionar(self):
        self.boxTotal.addWidget(QtGui.QLabel('<b>Defina</b> abaixo as preferencias do <b>BoTWiPy</b>'))

        self.boxTotal.addWidget(self.checkBoxRoda)
        self.boxTotal.addWidget(self.checkBoxMensoes)
        self.boxTotal.addWidget(self.checkBoxMsgSeg)

        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setGeometry(30, 40, 100, 30)
        self.sld.valueChanged[int].connect(self.changeValue)

        self.label = QtGui.QLabel('<b>0</b>')
        self.boxIntervalo.addWidget(QtGui.QLabel('<b>Intervalo</b>'))
        self.boxIntervalo.addWidget(self.sld)
        self.boxIntervalo.addWidget(self.label)

        self.boxBotao.addWidget(self.botaoGravar)
        self.boxBotao.addWidget(self.botaoCancelar)

        self.boxTotal.addLayout(self.boxIntervalo)
        self.boxTotal.addLayout(self.boxBotao)
        self.setLayout(self.boxTotal)

    def changeValue(self, value):
        self.label.setText('<b>{0}</b>'.format(int(value) + 1))

    def configurar(self):
        self.setModal(True)
        self.setWindowTitle('BoTWiPy - Preferencias')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        self.setFixedSize(310, 230)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)
        self.show()

    def gravar(self):
        a = open(settings.NOME).read()

        if str(self.checkBoxRoda.checkState()) == '2':
            bot.INIT = True
            a = re.sub('\nINIT(.*?)\n', '\nINIT = True\n', a)
        else:
            bot.INIT = False
            a = re.sub('\nINIT(.*?)\n', '\nINIT = False\n', a)
        if str(self.checkBoxMensoes.checkState()) == '2':
            bot.MENSOES = True
            a = re.sub('\nMENSOES(.*?)\n', '\nMENSOES = True\n', a)
        else:
            bot.MENSOES = False
            a = re.sub('\nMENSOES(.*?)\n', '\nMENSOES = False\n', a)
        if str(self.checkBoxMsgSeg.checkState()) == '2':
            bot.MSG_SEG = True
            a = re.sub('\nMSG_SEG(.*?)\n', '\nMSG_SEG = True\n', a)
        else:
            bot.MSG_SEG = False
            a = re.sub('\nMSG_SEG(.*?)\n', '\nMSG_SEG = False\n', a)

        bot.INTERVALO = int(self.sld.value()) + 1
        a = re.sub('\nINTERVALO(.*?)\n', '\nINTERVALO = {0}\n'.format(int(self.sld.value()) + 1), a)

        arq = open(settings.NOME, 'w')
        arq.write(a)
        arq.close()

        QtGui.QMessageBox.about(self, "Sucesso", "Preferencias Salvas")
        self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = JanelaInicial()
    sys.exit(app.exec_())
