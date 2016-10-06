'''
A script which takes two files as parameters.A file containing LiveTweets file as the first argument and other argument as
a file containing sentiment scores for each term
'''

import sys
import json
import csv
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
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#import classify
from importlib import reload
import mainfile
reload(mainfile)
from mainfile import query, query_location, dictionary, tweet_file, sentiment_location, wc_location
 
dic={}

print("Gathering Tweet Sentiment............")

def print_lines():
    x=0
    with open(dictionary) as f:
        lines=f.readline()
        while(lines!=''):
            lines=f.readline()
            line=lines.split('\t')
            if(len(line) >= 2):
                scores=line[1]
                dic[line[0]]=int(scores)


def tweet_sentiment_plot(cou,pos,neg,neu):
    plt.figure()
    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Positive', 'Negative', 'Neutral'
    values = [pos, neg, neu]
    sub_title="Gathered from a set of ", cou ,"Tweets"
    plt.pie(values, labels=labels, shadow=True, autopct='%.2f')
    plt.title(query.title() + ' Twitter Sentiment')
    plt.suptitle(sub_title, y=0.99, fontsize=12)
    plt.savefig(sentiment_location)

#Generate a WordCloud

def tweet_wordcloud():
    text = open(tweet_file).read()
    #text = " ".join(tweets['text'].values.astype(str))
    no_urls_no_tags = " ".join([word for word in text.split()
                                    if 'http' not in word
                                        and not word.startswith('@')
                                        and word != 'RT'
                                    ])
    wc = WordCloud(background_color="white", max_font_size=40, random_state=42, relative_scaling=.5).generate(no_urls_no_tags)
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(wc_location)
    
def tweet():
    count=0
    neu=0
    pos=0
    neg=0
    with open(query_location) as fp:
        for line in fp:
            tweet = json.loads(line)
            #print(tweet["text"])
            try:
                with open(tweet_file, "a") as f:
                    print(tweet["text"],file=f)
            except KeyError:
                continue
    with open(tweet_file) as tweetfile:
        #line=tweetfile.readline()
        for line in tweetfile:
            try:
            #while(line!=''and line!='\n'):
                scores=0
                tup=line.split(" ")
                if(len(tup)>=1):
                    for x in (tup):
                        if x in dic:
                            scores=scores + dic[x]
                            #print (scores)
                            count = count + 1                        
                            if scores > 1:
                                pos = pos +1
                            elif scores < 1:
                                neg = neg + 1
                            else:
                                neu+=1
            except KeyError:
                continue
    tweet_sentiment(count, pos, neg , neu)

def tweet_sentiment(c,p,n,ne):
    count=c
    positive=float(p/c)*100
    negative=float(n/c)*100
    neutral=float(ne/c)*100
    tweet_sentiment_plot(count,positive,negative,neutral)
    print ("Total tweets",c)
    #print ("Positive ",float(p/c)*100,"%")
    #print ("Negative ",float(n/c)*100,"%")
    #print ("Neutral ",float(ne/c)*100,"%")
    
#def tweet_cleaning():
   

def main():
    dic ={}
    open(tweet_file, "w")
    print_lines()
    tweet()
    print("Tweet Sentiment pie chart generated at:", sentiment_location)
    tweet_wordcloud()
    print("Tweet Word Cloud generated at:", wc_location)
if __name__ == '__main__':
    main()
