'''Gahters the hashtags and and shows the count on a graph'''
import json
import re
from mainfile import query, query_location, dictionary, hashtag_file, hashtag_graph
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

print("calculating Hashtag Count.........")
open(hashtag_file, "w")
cnt = Counter ();
keys_freq = []
values_freq = []
id_list = list()

'''Plots the Hashtag Bar Graph'''
def hashtag_plot(c):
	xaxis = range(len(c))
	for key, value in c.most_common()[::-1]:
	    keys_freq.append(key)
	    values_freq.append(value)

	fig = plt.figure()
	plt.subplot(211)
	plt.bar(xaxis, values_freq, align='center')
	plt.xticks(xaxis, keys_freq)
	locs, labels = plt.xticks()
	plt.setp(labels, rotation=90)
	fig.tight_layout()
	plt.savefig(hashtag_graph)

def clean_text(text):
    text = re.sub(r'\'+', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'(https?://[^\s]+)', ' ', text, flags=re.MULTILINE)
    text = re.sub('[$,?!\n]', ' ', text)
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    text = re.sub('[^A-Za-z0-9 ]+', ' ', text)
    return text

'''Recognizes and counts hashtags'''
with open(query_location) as f:
    for line in f:
        try:
            tweet = json.loads(line)
            if 'text' in tweet:
                idt = str(tweet['id'])
                #print (idt,"id")
                id_list.append(idt)
                text = str(tweet['text'])
                text = clean_text(text)
                hash_tags = []
                for hashtag in tweet['entities']['hashtags']:
                    ht = hashtag['text']
                    with open(hashtag_file,"a") as f:
                         print(ht,file=f)
        except KeyError:
            continue

for line in open (hashtag_file, 'r'):
  for word in line.split ():
    cnt [word] += 1
hashtag_plot(cnt)
