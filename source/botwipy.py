# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import time
import tweepy
import settings

# Adicionado as chaves no oauth.
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)

# Conectando a API utilizando os dados da aplicação.
api = tweepy.API(auth)

print 'Nome: {0}'.format(api.me().name)

replies = api.mentions()
for repli in replies:
    print repli
