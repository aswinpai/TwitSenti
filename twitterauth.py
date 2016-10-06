from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import sys
import os
import codecs
from importlib import reload
import mainfile


#consumer key, consumer secret, access token, access secret.
ckey="*************************"
csecret="**************************************************"
atoken="**************************************************"
asecret="*********************************************"

reload(mainfile)
from mainfile import query, query_location

class listener(StreamListener):
    def __init__(self, count):
        self.counter = 0
        self.limit = count

    def on_data(self, data):
        try:
            with open(query_location, 'a') as f:
                f.write(data)
                self.counter += 1
            if self.counter == self.limit:
                print ("Limit reached. Exiting...")
                return False
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print (status)

open(query_location, 'w').close()

if __name__ == '__main__':
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterstream = Stream(auth, listener(count=5000))
        print("Writing Tweets")
        twitterstream.filter(track=[query], languages=['en'])
    except KeyboardInterrupt:
        print ("Exiting....")
#That is enough to print out all of the data for the streaming live tweets that contain the term "car." We can use the json module to load the data var with json.loads(data), and then we can reference the tweet specifically with:
#tweet = all_data["text"]
