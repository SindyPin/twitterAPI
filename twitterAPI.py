# PASSO 1: Importar as bibliotecas necessárias
import tweepy
import datetime
import json
import time

import requests
from rq import Queue
from worker import conn

# PASSO 2: Importar a biblioteca que irá analizar polaridade, sentimento e subjetividade dos tweets
from textblob import TextBlob

# PASSO 3: Importar a classe TweetStore desde o documento tweetStore.py para estocar os tweets captados
from tweetStore import TweetStore

# PASSO 4: Importar os tokens e as senhas do Twitter Developer Account
from keys_twitter import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)
store = TweetStore()


#q = Queue(connection=conn)

# PASSO 5: Criar a classe Listener para as análises e filtragens necessárias
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Nota 1: A seguinte linha elimina os retweets para que sejam analisados somente os tweets      
        if 'RT @' not in status.text:
            # Nota 2: Análise das reações dos tweets:
            # Polaridade: Positivo / Negativo / Neutro
            # Subjetividade: Subjetivo / Objetivo
            # Emoção ou Sentimento: Chateado / Feliz / Triste / etc.
            blob = TextBlob(status.text)
            sent = blob.sentiment
            polarity = sent.polarity
            subjectivity = sent.subjectivity
            # Nota 3: Filtragens: id, texto, polaridade, subjetividade, nome de perfil, nome real, foto e data do tweet
            tweet_item = {'id_str': status.id_str,
                          'text': status.text,
                          'polarity': polarity,
                          'subjectivity': subjectivity,
                          'username': status.user.screen_name,
                          'name': status.user.name,
                          'profile_image_url': status.user.profile_image_url,
                          'received_at': datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')}
            # Nota 4: Puxar e printar os tweets estocados
            store.push(tweet_item)
            print("Pushed to redis:", tweet_item)
            # Nota 4: Outra forma de apresentar os resultados:
            # print('{name} ({username}) postou \n"{tweet}" \nno dia {date}.\n'
            # .format(name=status.user.name, username=status.user.screen_name, tweet=status.text,
            # date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        time.sleep(5)

    # Nota 5: "on_error" determina um limite de requerimentos dos tweets por hora para que o sistema não trave
    def on_error(self, status_code):
        if status_code == 420:
            return False


# PASSO 6: Chamar à função listener criada anteriormente
# PASSO 7: Filtrar os Twitters mais recentes com o comando "track"
# Nota 5: O comando "filter" pode filtrar os tweets por localidade, autor, língua do tweet e/ou hashtag
# Link com os parâmetros: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
# Exemplos:
# A) Filtrar tweets por região --> ex: filter(locations=[-73.504389, 41.222582, -71.804192, 42.026518])
# B) Filtrar tweets por @autor --> ex: filter(auth=['@SindyLicette'])
# C) Filtrar tweets por id do usuário con tweets próprios, retweetados e/ou resposta(s) a outros tweet --> ex:
# filter(follow=['2211149702']) / Link para encontrar os IDs dos autores: https://codeofaninja.com/tools/find-twitter-id
# D) Filtrar tweets por língua --> ex: filter(language=['pt-BR']):
# Link contendo todos os "Language Code Identifiers": https://github.com/libyal/libfwnt/wiki/Language-Code-identifiers
# E) Filtrar tweets por palavras e/ou frases
# Pode ser uma lista de palavras ou frases separadas por comas ou espaços,
# o qual representa OR e AND, respectivamente --> ex: filter(track['Enem', '#something'])
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['#vegan', '#MotivationMonday ', '#TravelTuesday', '#WCW', '#TBT', '#OOTD', '#TBH'])
