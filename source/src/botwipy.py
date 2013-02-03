
# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsavel pelas interacoes com a api do tweepy no software.
"""

import re
import time
import tweepy
import settings
import urllib2
import json
from redis import Redis


class BotAPI():
    """
    Classe responsavel por tratar as interacoes do bot.
    """

    def __init__(self):
        self.RODAR = True

        self.INIT = settings.INIT
        self.MENSOES = settings.MENSOES
        self.MSG_SEG = settings.MSG_SEG
        self.INTERVALO = settings.INTERVALO

        self.redis = Redis()
        self.redis.set('CONSUMER_KEY', settings.CONSUMER_KEY)
        self.redis.set('CONSUMER_SECRET', settings.CONSUMER_SECRET)
        self.redis.set('OAUTH_TOKEN', settings.OAUTH_TOKEN)
        self.redis.set('OAUTH_TOKEN_SECRET', settings.OAUTH_TOKEN_SECRET)

        auth = tweepy.OAuthHandler(self.redis.get('CONSUMER_KEY'), self.redis.get('CONSUMER_SECRET'), self.redis.get('OAUTH_TOKEN'))
        auth.set_access_token(self.redis.get('OAUTH_TOKEN'), self.redis.get('OAUTH_TOKEN_SECRET'))
        self.api = tweepy.API(auth)

    def carrega_api(self):
        """
        Carrega as chaves oauth e estabiliza um acesso com a api.
        Retorna verdadeiro caso as chaves estejam corretas, ou falso, caso contrario.
        """
        auth = tweepy.OAuthHandler(self.redis.get('CONSUMER_KEY'), self.redis.get('CONSUMER_SECRET'), self.redis.get('OAUTH_TOKEN'))
        auth.set_access_token(self.redis.get('OAUTH_TOKEN'), self.redis.get('OAUTH_TOKEN_SECRET'))
        self.api = tweepy.API(auth)

        if self.get_meu_nome() == None:
            return False
        else:
            return True

    def get_meu_nome(self):
        """
        Retorna o nome da conta que foi configurada.
        """
        try:
            return self.api.me().name
        except:
            return None
        
    def get_meu_status(self):
        """
        Retorna o status atual da conta que foi configurada.
        """
        return self.api.get_status(self.api.me().id).text

    def get_meus_tweets(self):
        """
        Retorna uma lista das ultimas 20 mensagens da conta que foi configurada.
        """
        return tweepy.Cursor(self.api.user_timeline).items()

    def get_amigos_tweets(self):
        """
        Retorna uma lista das ultimas 20 mensagens dos amigos da conta que foi configurada.
        """
        return self.api.friends_timeline()

    def seguir_usuario(self, usuario):
        """
        Segue um novo usuario a partir do parametro passado. Retorna uma mensagem
        de confirmacao, caso ele tenha consiguido ou nao seguir o usuario.
        """
        try:
            self.api.get_user(usuario).follow()
            return 'comecou a seguir {0}'.format(usuario)
        except:
            return 'nao conseguiu seguir {0}'.format(usuario)

    def verifica_tweet(self, tweet, condicao):
        """
        Analiza a mensagem, verificando se existe algum usuario.
        Se existe um usuario, ele o retorna, caso contrario, retorna None.
        """
        usuario = re.findall(r'{0}'.format(condicao), tweet.text)
        if (len(usuario) > 0):
            return [usuario[0], tweet.created_at]
        return None

    def get_seguidores(self):
        """
        Retorna uma lista com todos os seguidores da conta configurada.
        """
        seguidores = tweepy.Cursor(self.api.followers, id = self.api.me().id)
        lista = []
        for seguidor in seguidores.items():
            lista.append(seguidor.screen_name)
        return lista

    def get_mensoes(self):
        """
        Obtem uma lista de todos as mensoes existentes no twitter em uma lista.
        """
        minhas_mensoes = tweepy.Cursor(self.api.mentions).items()
        lista = []
        for status in minhas_mensoes:
            lista.append([status.user.id, status.user.screen_name, status.text, status.created_at])
        return lista

    def send_mensagem(self, usuario, mensagem):
        """
        Envia uma mensagem para um determinado usuario.
        """
        self.api.send_direct_message(user_id = usuario, text = mensagem)

    def atualizar_status(self, mensagem):
        """
        Atualizar o Status da conta que foi configurada.
        """
        try:
            self.api.update_status(mensagem)
        except:
            pass