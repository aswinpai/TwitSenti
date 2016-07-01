import json
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import urllib
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import re
import os
import sys
import time
import collections
from importlib import reload
import mainfile
import classify

reload(mainfile)
from mainfile import query, query_location

#Checks if the word is found of not
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

#extracts link from tweet by checking for http
def extract_link(text):
    regex=r'((https?|www?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
    #regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

#define file
#tweets_data_path = 'modi.json'

#create array and read tweets
tweets_data = []
hashtagList = []
tweets_file = open(query_location, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
        for hashtag in tweet['entities']['hashtags']:
            hashtagList.append(hashtag['text'])
        #create a dataframe
        #only map gives an error because json donet have all fields. Use List
        tweets = pd.DataFrame()
        tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
        #tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
        #tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data))
        tweets['country'] = list(map(lambda tweet: tweet.get('place', {}).get('country') if tweet.get('place', None) != None else None, tweets_data))
        tweets_by_country = tweets['country'].value_counts()
        #print collections.Counter(hashtagList)
        #checks for the word in the tweet and prints the count
        tweets[query] = tweets['text'].apply(lambda tweet: word_in_text(query, tweet))
        #print (tweets['egypt'].value_counts()[True])
        #only prints top 10 tweets
        #print(tweets['text'][:10])
        #define dataframe link
        tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))
        #define relavance and the basis of relavance
        tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text(query, tweet))
        tweets_relevant = tweets[tweets['relevant'] == True]
        tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']
        text = " ".join(tweets['text'].values.astype(str))
    except KeyError:
        continue

#gives the number of tweets
print ("total tweets")
print (len(tweets_data))


#Generate a WordCloud
#text = " ".join(tweets['text'].values.astype(str))
no_urls_no_tags = " ".join([word for word in text.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'
                                ])
wc = WordCloud(max_font_size=40, relative_scaling=.5).generate(no_urls_no_tags)
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.savefig('wc.png')

#Analysis of URL's begins here
lis=[]
open("output.txt","w")
open("out.txt", "w")
#Outputs to a file out.txt
with open("out.txt", "a") as f:
    print (tweets_relevant_with_link[tweets_relevant_with_link[query] == True]['link'], file=f)
    
reload(classify)
from classify import cl

#checks and matches each links and out puts proper links to another file
#TODO - consider deleting old file after the operation has ended
with open("out.txt") as f:
    for line in f:        
        try:
            #Checks each line for anything with https
            tlink = (re.search("(?P<url>https?://[^\s]+)",line).group("url"))
            #Checks if line has 23 chars. All links from twitter have 23 chars. This would avoid broken links
            if (len(tlink)==23):
                with open("output.txt","a") as linkfile:
                    #Prints link to another file
                    print(tlink)
                    #Runs the link through beautiful soup
                    #soup = BeautifulSoup(urllib.request.urlopen(tlink), "lxml")
                    #Runs the title of each link through wordblob
                    #blob = TextBlob(soup.title.string)
                    #url = "https://t.co/GidwDxbCYB"
                    #html = urllib.request.urlopen(tlink).read()
                    soup = BeautifulSoup(urllib.request.urlopen(tlink).read(),'html.parser')
                    # kill all script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()    # rip it out
                    # get text
                    text = soup.get_text()
                    # break into lines and remove leading and trailing space on each
                    lines = (line.strip() for line in text.splitlines())
                    # break multi-headlines into a line each
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    # drop blank lines
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    #encoded_text = text.encode('utf-8')
                    blob = TextBlob(text)
                    #print (blob.sentiment.polarity)
                    #print (soup.title.string)
                    #Sentiment analysis of each link
                    #lis.append(blob.sentiment.polarity)
                    if blob.sentiment.polarity < 0:
                        print (tlink, ": Negative")
                    if blob.sentiment.polarity == 0:
                        print (tlink, ": Neutral")
                    elif blob.sentiment.polarity > 0:
                        print (tlink, ": Positive")
        except:
            tlink = None
linkfile.close()
f.close()