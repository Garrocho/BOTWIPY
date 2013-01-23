# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import re
import time
import tweepy
import settings
import urllib2
import json
from os import system


class BotAPI(tweepy.API):

    def __init__(self):
        self.RODAR = settings.RODAR
        self.MENSOES = settings.MENSOES

        # Adicionado as chaves no oauth.
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)
        super(BotAPI, self).__init__(auth)
                
    def get_meu_nome(self):
        return self.me().name
        
    def get_meu_status(self):
        return self.get_status(self.me().id).text

    def get_meus_tweets(self):
        return tweepy.Cursor(self.user_timeline).items()

    def get_amigos_tweets(self):
        return self.friends_timeline()

    def seguir_usuario(self, usuario):
        try:
            self.get_user(usuario).follow()
            return 'comecou a seguir {0}'.format(usuario)
        except:
            return 'nao conseguiu seguir {0}'.format(usuario)

    def verifica_tweet(self, tweet, condicao):
        usuario = re.findall(r'{0}'.format(condicao), tweet.text)
        if (len(usuario) > 0):
            return [usuario[0], tweet.created_at]
        return None

    def get_seguidores(self):
        seguidores = tweepy.Cursor(self.followers, id = self.me().id)
        lista = []
        for seguidor in seguidores.items():
            lista.append(seguidor.screen_name)
        return lista

    def get_mensoes(self):
        minhas_mensoes = tweepy.Cursor(self.mentions).items()
        lista = []
        for status in minhas_mensoes:
            lista.append([status.user.id, status.user.screen_name, status.text])
        return lista

    def send_mensagem(self, usuario, mensagem):
        self.send_direct_message(user_id = usuario, text = mensagem)

    def atualizar_status(self, mensagem):
        try:
            self.update_status(mensagem)
        except:
            pass
