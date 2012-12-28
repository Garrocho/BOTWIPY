# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import re
import time
import tweepy
import settings

# Adicionado as chaves no oauth.
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)

# Conectando a API utilizando os dados da aplicação.
api = tweepy.API(auth)

print 'Meus Dados'
print 'Nome: {0}'.format(api.me().name)

mensagens = tweepy.Cursor(api.user_timeline).items()

print '\nMinhas Mensagens'
for status in mensagens:
    print status.text

# Verificando as mensagens com Via referência e adicionando esses usuários.
msm_amigos = api.friends_timeline()
for mensagem in msm_amigos:
    if '( via @' in mensagem.text:
        usuario = re.findall(r'via @(.*?)\)', mensagem.text)[0]
        api.get_user(usuario).follow()
        print '{0} começou a seguir {1}'.format(api.me().name, usuario)
