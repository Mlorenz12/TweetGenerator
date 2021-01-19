import pandas as pd
import numpy as np 
import random
import json
import logging
import torch
from random import shuffle, randint
#import tensorflow as tf
#from keras.layers import LSTM,Embedding
from torch import nn, optim
#from collections import Counter#wozu?
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.basicConfig(filename='unixmen.log', level=logging.DEBUG)
logging.info('INfo')
logging.error('Error')
logging.critical('Critical')
logging.debug('Debug')
print('imports fertig')

'''
Punkte müssen ja drin gelassen werden, damit Sätze verbunden werden können, genauso wie ", damit direkte Sprache?
--> wegen " mal schauen wie das theoretisch gehen würde, beziehungsweise wie Daten aufbereitet werden müssten?
--> Herausfinden wie man eigentlich Daten aufbereitet in NLP?
'''
def process_data(data):
    '''
    data: string of unprocessed text input
    '''
    data = data.split(' ')
    #preparation of data, removing special characters from beginning and ending of words
    data = [word.strip('\n') for word in data]
    #nach Satzzeichen im Satzflow checken (hier mal noch was einfügen)
    for word in data:
        if word.startswith('"'):
            pass
        if word.endswith('"'):
            pass
            if word.endswith('?'):
                pass
            elif word.endswith('!'):
                pass
            else:
                pass
        if word.endswith(','):
            pass
        elif word.endswith('.'):
            pass
    data = [word.strip(',') for word in data]
    data = [word.strip('?') for word in data]
    data = [word.strip('!') for word in data]
    data = [word.strip('.') for word in data]
    data = [word.strip('."') for word in data]
    data = [word.strip('?"') for word in data]
    data = [word.strip('!"') for word in data]
    data = [word for word in data if word != '']#remove empty strings
    return data


def get_input_target(data, amount_words = 15):
    #amount_words: amount of words in a input/target sequence
    result = []#list containing input + target seuqnces
    words = len(data)
    start_idx = 0
    end_idx = start_idx + amount_words

    for iteration in range(words-amount_words):
        '''
        hier sind jetzt satzzeichen (dadurch dass die mit dem strip befehl alle gelöscht wurden)
        nicht relevant, die frage ist ob man eine liste mit bereinigten Wörtern macht, die dann im corpus 
        speichert und dann die satzzeichen " oder , oder ! ? . etc irgendwie wie "richtige" Wörter im Text 
        behandelt (schauen ob es da eine funktion/Möglichkeit gibt das umzusetzen) 
        '''
        input_sequence = data[start_idx:end_idx]
        '''
        nachsehen ob input wirklich nur so klein ist?
        '''
        input_mapped = np.zeros(amount_words)
        for c,inp in enumerate(input_sequence):
            input_mapped[c] = corpus_reverse[inp]
        '''
        dataX wird reshaped und normalized??? ---> Was wird hier normalized und wo wirds hin geshaped?
        '''
        target_sequence = data[start_idx+1:end_idx+1]
        target_hot = np.zeros(len(corpus))#hier werden Satzzeichen wie ., etc die die halt oben sind schon berücksichtigt!
        for target in target_sequence:
            '''
            FRAGE: Was ist wenn Wörter doppelt vor kommen?
            Wird das doppelte Wort dann trotzdem nur einmal encoded? Probably yes?
            '''
            target_hot[corpus_reverse[target]] = 1
        result.append((input_mapped, target_hot))#save input and target as tuple in list
        start_idx += 1
        end_idx = start_idx +amount_words

    return result

#tweets = []#liste für alle tweets, enthält nur ein Dictionary
#count = 0
for line in open('trump.json', 'r', encoding="utf8"):#einlesen jedes einzelnen tweets 
    tweets = json.loads(line)#umwandeln des json strings in ein dictionary und hinzufügen zu liste
print('Anzahl Tweets: {}'.format(len(tweets)))

tweets_ = list(tweets.values())
print('hinter liste tweets')
trump = ' '.join(tweets_)
trump = process_data(trump)
corpus = {key:value for key,value in enumerate(list(set(trump)))}#take unique words from hp book and map it to an index, ordnet index ein wort zu
corpus_reverse = {value:key for key,value in enumerate(list(set(trump)))}#ordnet wörtern einen index zu
print('hinter corpus')
input_target_list = get_input_target(trump)
shuffle(input_target_list)
print('ist fertig...')