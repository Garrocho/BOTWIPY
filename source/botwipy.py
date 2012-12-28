# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

import re
import time
import tweepy
import settings

class BotAPI(tweepy.API):

    def __init__(self, auth):
        super(BotAPI, self).__init__(auth)

    def get_meu_nome(self):
        return self.me().name()

    def get_meus_tweets(self):
        return tweepy.Cursor(api.user_timeline).items()

    def get_amigos_tweets(self):
        return api.friends_timeline()

    def seguir_usuario(self, usuario):
        self.get_user(usuario).follow()

    def verifica_tweet(self, tweet, condicao):
        usuario = re.findall(r'{0}(.*?):'.format(condicao), tweet.text)
        if (len(usuario) > 0):
            return usuario[0]
        return None


if __name__ == '__main__':

    # Adicionado as chaves no oauth.
    print 'Definindo Chaves de Acesso do BOT...'
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)

    # Conectando a API utilizando os dados da aplicação.
    print 'Autenticando BOT no AUTH...'
    api = BotAPI(auth)

    # Verificando as mensagens com Via referência e adicionando esses usuários.
    print 'Entrando no Loop para Verificar Novos Tweets'
    while True:
        time.sleep(2)
        amigos_tweets = api.get_amigos_tweets()
        for tweet in amigos_tweets:
            usuario = api.verifica_tweet(tweet, 'RT @')
            if usuario is not None:
                api.seguir_usuario(usuario)
                print '{0} começou a seguir {1}'.format(api.me().name, usuario)
