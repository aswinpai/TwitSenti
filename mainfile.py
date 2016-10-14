import os
import sys

#inputs
location = os.getcwd()
#Input the query here. Hardcoading now. Taken from GUI later
query='whatever'
#Locations of outputs
query_location=location + '/input/' + query +'.json'
dictionary=location+ '/input/' +'AFINN-111.txt'
tweet_file=location+ '/output/' +'tweet_out.txt'
sentiment_location=location+ '/output/' +'sentiment.png'
wc_location=location+ '/output/' +'wc.png'
url_sentiment=location+ '/output/' +'url_sentiment.txt'
hashtag_file=location+ '/output/' +'hashtag.txt'
hashtag_graph=location+ '/output/' +'hashtag.png'

