# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import os

# Nome do Arquivo Atual.
NOME = '{0}.py'.format(os.path.abspath(__file__).split('.')[0])

# Defina Aqui o Estado Inicial do Bot
RODAR = False
MENSOES = False

# Consumer Key
CONSUMER_KEY = 'fE5bvsY0CEsoy9WUhCEpLw'
CONSUMER_SECRET = 'JegRGulzhvp09grgBtPNaMeuvyPvYKwTkPRrz0X1c'

# Access Token
OAUTH_TOKEN = '1024579182-pBEpPE8SyZjplZJHbPE64G3dcskSlUZYWutOpo2'
OAUTH_TOKEN_SECRET = 'aE6RBQl8HtZ9auMPEvTtN7R9dZ2oqp1WI5vXONs'

# Endereco principal do source do projeto.
PATH = os.getcwd().split('/src')[0]
ICON = 'icon/'
ARQ = 'arq/'

# Endereco de cada icone do projeto.
INICIAR = '{0}/{1}/{2}'.format(PATH, ICON, 'INICIAR.png')
PARAR = '{0}/{1}/{2}'.format(PATH, ICON, 'PARAR.png')
CHAVES = '{0}/{1}/{2}'.format(PATH, ICON, 'CHAVES.png')
CONFIGURAR = '{0}/{1}/{2}'.format(PATH, ICON, 'CONFIGURAR.png')
AJUDA = '{0}/{1}/{2}'.format(PATH, ICON, 'AJUDA.png')
FOLLOWERS = '{0}/{1}/{2}'.format(PATH, ICON, 'FOLLOWERS.png')
SAIR = '{0}/{1}/{2}'.format(PATH, ICON, 'SAIR.png')
ATUALIZAR = '{0}/{1}/{2}'.format(PATH, ICON, 'ATUALIZAR.png')
LOGO = '{0}/{1}/{2}'.format(PATH, ICON, 'LOGO.png')
FOLLOW = '{0}/{1}/{2}'.format(PATH, ICON, 'FOLLOW.png')

GRAVAR = '{0}/{1}/{2}'.format(PATH, ICON, 'GRAVAR.png')
CANCELAR = '{0}/{1}/{2}'.format(PATH, ICON, 'CANCELAR.png')
LIMPAR = '{0}/{1}/{2}'.format(PATH, ICON, 'LIMPAR.png')

# Endereco de arquivo do projeto.
HTML = '{0}/{1}/{2}'.format(PATH, ARQ, 'index.html')
