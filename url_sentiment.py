from bs4 import BeautifulSoup
import urllib
import csv
import re
from importlib import reload
import mainfile
reload(mainfile)
from mainfile import query, query_location, dictionary, tweet_file, url_sentiment


print("URL Sentiment Analysis........")
print("This might take a while......."
open(url_sentiment, "w")

dic={}
x=0
url_list=[]

with open(dictionary) as f:
    lines=f.readline()
    while(lines!=''):
        lines=f.readline()
        line=lines.split('\t')
        if(len(line) >= 2):
            scores=line[1]
            dic[line[0]]=int(scores)


with open(tweet_file) as f:
        for line in f:        
            try:
                #Checks each line for anything with https
                tlink = re.search("(?P<url>https?://[^\s]+)", line).group("url")
                if (len(tlink)==23):
                    soup = BeautifulSoup(urllib.request.urlopen(tlink).read(),'html.parser')
                    # kill all script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()    # rip it out
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    # break multi-headlines into a line each
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    # drop blank lines
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    scores=0
                    tup=text.split(" ")
                    if(len(tup)>=1):
                        for x in (tup):
                            if x in dic:
                                scores=scores + dic[x]
                        if scores > 1:
                            with open(url_sentiment, "a") as f:
                                print(tlink,scores,"Positive", file=f)
                        elif scores < 1:
                            with open(url_sentiment, "a") as f:
                                print(tlink,scores,"Negative", file=f)
                        else:
                            with open(url_sentiment, "a") as f:
                                print(tlink,scores,"Neutral", file=f)
            except:
                tlink = None
