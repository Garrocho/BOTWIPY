# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsavel pelas interfaces graficas utilizadas no software.
"""

import re
import sys
import time
import settings
import botwipy
import sys
from datetime import date
from threading import Thread
from PyQt4 import QtGui, QtCore, QtWebKit, Qt

# Conectando a API utilizando os dados da aplicação.
global bot
bot = botwipy.BotAPI()
encoding = sys.getfilesystemencoding()


class IniciarBot(QtCore.QThread):
    """
    Processo responsavel por iniciar e analisar as mensagens do BoTWiPy.
    """
    mensagem_lista = QtCore.pyqtSignal(str)
    mensagem_status_bar = QtCore.pyqtSignal(str)

    def run(self):
        """
        Executa o processo de Iniciar o Bot.
        """

        self.mensagem_status_bar.emit('Analisando as Chaves do BoTWiPy')
        if bot.carrega_api() == True:

            while bot.RODAR:

                try:

                    if bot.MSG_SEG == True:
                        self.mensagem_status_bar.emit('Analisando a Lista de Mensagens das Pessoas Que Eu Sigo...')
                        amigos_tweets = bot.get_amigos_tweets()
                        for tweet in amigos_tweets:
                            if bot.RODAR:
                                self.mensagem_status_bar.emit(tweet.text)
                                usuario = bot.verifica_tweet(tweet, 'RT @(.*?):')
                                if usuario is not None:
                                    dt = date.today()
                                    self.mensagem_lista.emit('<b>{0}</b> <i>{1}</i> <br>{2}'.format(bot.get_meu_nome(), dt.strftime("%d de %B de %Y"), bot.seguir_usuario(usuario[0])))
                            else:
                                raise

                    if bot.MENSOES == True:
                        self.mensagem_status_bar.emit('Analisando a Lista de Minhas Mensoes...')
                        for usuario in bot.get_mensoes():
                            if bot.RODAR:
                                self.mensagem_status_bar.emit(usuario[1] + ': ' + usuario[2])
                                dt = date.today()
                                self.mensagem_lista.emit('<b>{0}</b> <i>{1}</i> <br>{2}'.format(bot.get_meu_nome(), dt.strftime("%d de %B de %Y"), bot.seguir_usuario(usuario[1])))
                                novo_status = u'Ola @{0}. Obrigado pela sua mensagem! :-)'.format(usuario[1])
                                self.mensagem_lista.emit('<b>{0}</b> <i>{1}</i> <br> Atualizou seu Status para: {2}'.format(bot.get_meu_nome(), dt.strftime("%d de %B de %Y"), novo_status))
                                bot.atualizar_status(novo_status)
                            else:
                                raise

                    self.mensagem_status_bar.emit('Entrando no Estado de Intervalo... {0} minutos de espera'.format(bot.INTERVALO))
                    intervalo = bot.INTERVALO
                    for i in range(intervalo):
                        if bot.RODAR:
                            for i in range(60):
                                if bot.RODAR:
                                    time.sleep(1)
                                    intervalo -= 1
                                else:
                                    raise
                            self.mensagem_status_bar.emit('Estado de Intervalo... {0} minutos de espera'.format(intervalo))
                        else:
                            raise
                except:
                    pass
                self.mensagem_status_bar.emit('Saindo do Estado de Intervalo...')
        else:
            self.mensagem_status_bar.emit('ERRO')


class PararBot(QtCore.QThread):
    """
    Processo responsavel por parar a execucao do BoTWiPy
    """
    mensagem_status_bar = QtCore.pyqtSignal(str)
    
    def run(self):
        """
        Inicia o processo de parar a execucao do bot.
        """
        bot.RODAR = False
        self.mensagem_status_bar.emit('Parando o BoTWiPy')


class JanelaInicial(QtGui.QMainWindow):
    """
    Essa é a Interface gráfica inicial do botwipy. Nela é definido uma barra de
    botões o carregamento de uma lista de um arquivo html e a barra de status.
    """

    def __init__(self):
        """
        Realiza a contrucao da janela inicial do software.
        """
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
            self.iniciarBot.setEnabled(False)
        else:
            self.parar_bot()
            self.pararBot.setEnabled(False)
                        
        self.configurar()
   
    def recebe_msg_init_lista(self, mensagem):
        """
        Recebe uma mensagem e chama uma funcao do arquivo html passando como argumento a mensagem.
        """
        self.webView.page().mainFrame().evaluateJavaScript('novoElemento("%s")' % (mensagem,))
        self.atuaBot.setEnabled(True)

    def recebe_msg_init_status(self, mensagem):
        """
        Recebe uma mensagem e chama adiciona a mensagem na barra de status.
        """
        if mensagem == 'ERRO':
            QtGui.QMessageBox.about(self, "Erro", "Impossivel Iniciar o BoTWiPy\nChaves Incorretas")
        else:
            self.statusBar().showMessage(mensagem)

    def iniciar(self):
        """
        Realiza a instancia de varios componentes da janela inicial.
        """
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
        self.atuaBot.setEnabled(False)
        
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
        """
        Adiciona todos os componentes na janela inicial.
        """
        
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
        """
        Configura todos os componentes da janela incial.
        """
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
        """
        Inicia o processo do Bot.
        """
        bot.RODAR = True
        self.iniciarBot.setEnabled(False)
        self.pararBot.setEnabled(True)
        self.pIniciar.start()

    def parar_bot(self):
        """
        Para o processo do Bot.
        """
        self.pParar.start()
        self.iniciarBot.setEnabled(True)
        self.pararBot.setEnabled(False)
    
    def limpar_lista(self):
        """
        Chama uma função no arquivo html para limar a lista de mensagens.
        """
        self.webView.page().mainFrame().evaluateJavaScript('LimparLista()')
        self.atuaBot.setEnabled(False)
    
    def chamar_sobre(self):
        """
        Chama o dialogo Sobre.
        """
        exSobre = DialogoSobre()
        exSobre.exec_()

    def chamar_chaves(self):
        """
        Chama o dialogo Configuracao de Chaves de Seguranca.
        """
        exChaves = DialogoChaves()
        exChaves.exec_()

    def chamar_preferencias(self):
        """
        Chama o dialogo de preferencias do bot.
        """
        exPreferencias = DialogoPreferencias()
        exPreferencias.exec_()


class DialogoSobre(QtGui.QDialog):
    """
    Essa é a Interface gráfica do dialogo sobre, onde contém as informações de
    software. Nela é definido vários rótulos e uma imagem logo do software.
    """
    
    def __init__(self):
        """
        Realiza a contrucao da janela, chamando os metodos de construcao.
        """
        super(DialogoSobre, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
        """
        Realiza a instancia de varios componentes da janela.
        """
        self.vbox = QtGui.QHBoxLayout()                                        
        self.setLayout(self.vbox)
          
        self.foto_label = QtGui.QLabel()
        self.foto_label.setPixmap(QtGui.QPixmap(settings.LOGO))
        self.label = QtGui.QLabel('<H3>Informacoes do software</H3> <b>Software: </b>Bot Twitter em Python <br> <b>Versao: </b> 1.0 <br> <b>Copyright: </b>Open Source<br> <H3>Desenvolvedores</H3> Charles Tim Batista Garrocho <br>Paulo Vitor Francisco')
        
    def adicionar(self):
        """
        Adiciona todos os componentes na janela inicial.
        """
        self.vbox.addWidget(self.foto_label)
        self.vbox.addWidget(self.label)

    def configurar(self):
        """
        Configura todos os componentes da janela.
        """
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
        """
        Realiza a contrucao da janela, chamando os metodos de construcao.
        """
        super(DialogoChaves, self).__init__()
        self.iniciar()
        self.adicionar()
        self.configurar()
        
    def iniciar(self):
        """
        Realiza a instancia de varios componentes da janela.
        """
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
        """
        Adiciona todos os componentes na janela inicial.
        """
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
        """
        Configura todos os componentes da janela.
        """
        self.setModal(True)
        self.setWindowTitle('BoTWiPy - Chaves de Seguranca')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        self.setFixedSize(400, 240)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)
        self.show()

    def gravar(self):
        """
        Grava os dados modificados no arquivo settings.
        """
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
        """
        Limpa os dados dos campos de texto da janela.
        """
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
        """
        Realiza a contrucao da janela, chamando os metodos de construcao.
        """
        super(DialogoPreferencias, self).__init__()
        self.iniciar()
        self.adicionar()
        self.sld.setValue(bot.INTERVALO)
        self.configurar()
        
    def iniciar(self):
        """
        Realiza a instancia de varios componentes da janela.
        """
        self.boxTotal = QtGui.QVBoxLayout()
        self.boxCheckBox = QtGui.QVBoxLayout()
        self.boxIntervalo = QtGui.QHBoxLayout()
        self.boxBotao = QtGui.QHBoxLayout()

        self.checkBoxRoda = QtGui.QCheckBox('Iniciar BoTWiPy ao executar', self)
        if bot.INIT == True:
            self.checkBoxRoda.toggle()

        self.checkBoxMensoes = QtGui.QCheckBox('Analisar Mensoes ao BoTWiPy', self)
        if bot.MENSOES == True:
            self.checkBoxMensoes.toggle()

        self.checkBoxMsgSeg = QtGui.QCheckBox('Analisar Mensagens Followers', self)
        if bot.MSG_SEG == True:
            self.checkBoxMsgSeg.toggle()

        self.botaoGravar = QtGui.QPushButton(QtGui.QIcon(settings.GRAVAR), 'Gravar')
        self.botaoGravar.setIconSize(QtCore.QSize(30,30));
        self.botaoGravar.clicked.connect(self.gravar)
        
        self.botaoCancelar = QtGui.QPushButton(QtGui.QIcon(settings.CANCELAR), 'Cancelar')
        self.botaoCancelar.setIconSize(QtCore.QSize(30,30));
        self.botaoCancelar.clicked.connect(self.close)

    def adicionar(self):
        """
        Adiciona todos os componentes na janela inicial.
        """
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
        """
        Modifica o valor do label de contagem.
        """
        self.label.setText('<b>{0}</b>'.format(int(value) + 1))

    def configurar(self):
        """
        Configura todos os componentes da janela.
        """
        self.setModal(True)
        self.setWindowTitle('BoTWiPy - Preferencias')
        self.setWindowIcon(QtGui.QIcon(settings.LOGO))
        self.setFixedSize(310, 230)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)
        self.show()

    def gravar(self):
        """
        Grava os dados modificados no arquivo settings.
        """
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
