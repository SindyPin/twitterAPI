# PASSO 1: Importar as biblitoecas e as funções necessárias
import os
import redis
import json

from rq import Queue
# from worker import conn
# from tweet import Tweet
# from twitterAPI import StreamListener

# PASSO 2: Criar variável para envio dos dados coletados a Reddis
# q = Queue(connection=conn)
# result = q.enqueue(StreamListener, 'https://twitter-api-final.herokuapp.com')

# PASSO 3: Criar uma classe contendo as funções necessárias para guardar os tweets captados
class TweetStore:

    # PASSO 4: Configurar Redis
    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    # PASSO 5: Configurar a quantidade de Tweets armazenados 
    # Nota 1: cada 100 tweets, eliminar a quantidade necessária de tweets para que o db sempre fique com pelo menos 20
    redis_key = 'tweets'
    num_tweets = 20
    trim_threshold = 100

    # PASSO 6: Criar a função __init__ para inicializar conexão com o db via Redis
    # Nota 2: "trim_count" elimina os tweets antigos do db para deixar entrar novos tweets
    def __init__(self):
    	#self.db = r = redis.Redis(host=self.redis_host, port=self.redis_port, password=self.redis_password)
    	self.trim_count = 0
    	self.db = r = redis.Redis.from_url(os.getenv('REDIS_URL', 'redis://h:pb857b6aec997348dae5b563101c5bd848c7035a575e659310d850cc090ef2394@ec2-3-82-83-129.compute-1.amazonaws.com:23679'))
    	#self.result = q.enqueue(StreamListener, 'https://twitter-api-final.herokuapp.com')
    # PASSO 7: Criar a função "tweets" que servirá para conectar o db ao servidor via web app
    # Nota 3: Na web app serão apresentados somente os últimos 15 tweets (dado pelo comando "limit")
    def tweets(self, limit=15):
        tweets = []
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            # Criar uma instância da classe tweet_obj importada do arquivo tweets.py
            tweet_obj = json.loads(item)
            tweets.append(Tweet(tweet_obj))
        return tweets

    # PASSO 8: Criar a função "push" para puxar os tweets desde https://twitter.com
    # Nota 4: "data" corresponde aos tweets que serão puxados 
    # (é um "tweet_object" que foi criado no arquivo de filtragem de tweets) 
    # Nota 5: "lpush" (left push) é o comando que puxará os tweets ao começo da API
    # (atualização dos últimos tweets de cima apra baixo)
    # Nota 6: "dumps" serve para despejar os tweets antigos e não sobrecarregar a API
    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1
        # Nota 7: O seguinte conjunto de comandos corta periodicamente tweets do db para que não cresça em excesso 
        # Quando atingir os 100 tweets, "trim_count" cortará tweets e deixará no db pelo menos 20 tweets
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0
