# PASSO 1: Importar o módulo re
# Nota: "Re" fornece operações de correspondência de expressões regulares semelhantes às encontradas no Perl
# Ver https://docs.python.org/3/library/re.html
import re


# PASSO 2: Definir a classe "Tweet" contendo as funções necessárias para captar e guardar os Tweets
# Nota: A classe "Tweet" apresenta métodos que auxiliam com o display dos dados
class Tweet:
    # PASSO 3: Criar a função "__init__" para inicializar conexão com o db
    def __init__(self, data):
        self.data = data

    # PASSO 4: Criar a função "user_link" para inicializar conexão via web
    def user_link(self):
        return "http://twitter.com/{}".format(self.data['username'])

    # PASSO 5: Criar a função "filtered_text" para filtrar os textos dos tweets
    def filtered_text(self):
        return self.filter_hashtags(self.filter_urls(self.data['text']))

    # PASSO 6: Criar a função "filter_hashtags" para filtrar as notícias dos jornais selecionados
    def filter_hashtags(self, text):
        hashtags = ['#vegan', '#MotivationMonday ', '#TravelTuesday', '#WCW', '#TBT', '#OOTD', '#TBH']
    # PASSO 7: Adicionar o tag correspondente para cada tweet relacionando-o com um sentimento, pode ser:
    # positivo (borda da caixa de cor verde), negativo (borda da caixa de cor vermelha) ou neutro (mesma cor)
        for h in hashtags:
            if h in text:
                text = text.replace(h, "<mark>{}</mark>".format(h))
            else:
                continue

        return text

    # PASSO 8: Criar a função "filter_urls" que encontra qualquer link e o substitue por uma tag para obter um botão
    # (para atualizar os tweets)
    def filter_urls(self, text):
        return re.sub("(https?:\/\/\w+(\.\w+)+(\/[\w\+\-\,\%]+)*(\?[\w\[\]]+(=\w*)?(&\w+(=\w*)?)*)?(#\w+)?)",
                      r'<a href="\1" target="_blank">\1</a>', text)
