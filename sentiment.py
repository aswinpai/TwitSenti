import json
import re
import operator 
from textblob import TextBlob
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
import os, sys, codecs
from nltk import bigrams
import classify
from importlib import reload
import mainfile

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def plotpie(pos,neg,neu):
    plt.figure()
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Positive', 'Negative', 'Neutral'
    values = [pos, neg, neu]
    plt.pie(values, labels=labels, shadow=True, autopct='%.2f')
    plt.title(query.title() + ' Twitter Sentiment')
    plt.savefig('sentiment.png')

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

reload(mainfile)
reload(classify)
from mainfile import query, query_location
from classify import cl

with open(query_location, 'r') as f:
    lis=[]
    ten=[]
    neg=0.0
    n=0.0
    net=0.0
    pos=0.0
    p=0.0
    count_all = Counter()
    cout=0
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        #tweet = tweet.encode('utf-8')
        try:
            blob = TextBlob(tweet["text"], classifier=cl)
            #print((blob, blob.classify())[:10])
            cout+=1
            lis.append(blob.sentiment.polarity)
            #print blob.sentiment.subjectivity
            #print (os.listdir(tweet["text"]))
            if blob.sentiment.polarity < 0:
                sentiment = "negative"
                neg+=blob.sentiment.polarity
                n+=1
            elif blob.sentiment.polarity == 0:
                sentiment = "neutral"
                net+=1
            else:
                sentiment = "positive"
                pos+=blob.sentiment.polarity
                p+=1
        except KeyError:
            continue
            
    # output sentiment
    pos=float(p/cout)*100
    neg=float(n/cout)*100
    neu=float(net/len(lis))*100
    plotpie(pos,neg,neu)
    print ("Total tweets",len(lis))
    print ("Positive ",float(p/cout)*100,"%")
    print ("Negative ",float(n/cout)*100,"%")
    print ("Neutral ",float(net/len(lis))*100,"%")