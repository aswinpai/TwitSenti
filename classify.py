from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

train = [
    ('I love this sandwich.', 'pos'),
    ('I hate this sandwich.', 'neg')
    ('This is an amazing place!', 'pos'),
    ('I feel very good about these beers.', 'pos'),
    ('This is my best work.', 'pos'),
    ("What an awesome view", 'pos'),
    ('I do not like this restaurant', 'neg'),
    ('I am tired of this stuff.', 'neg'),
    ("I can't deal with this", 'neg'),
    ('He is my sworn enemy!', 'neg'),
    ('My boss is horrible.', 'neg'),
    ('He won the election', 'pos'),
    ('This movie is great', 'pos'),
    ('There was a gun shooting', 'neg'),
    ('He is an Asshole.', 'neg'),
    ('The plane crashed', 'neg'),
    ("Development is good", 'pos'),
    ("People are supporting",'pos')
]
test = [
    ('The beer was good.', 'pos'),
    ('The beer was bad.', 'neg'),
    ('I do not enjoy my job', 'neg'),
    ("I ain't feeling dandy today.", 'neg'),
    ("I feel amazing!", 'pos'),
    ('Gary is a friend of mine.', 'pos'),
    ("I can't believe I'm doing this.", 'neg'),
    ("He is working on the development of the country.", 'pos'),
    ("Hillary won the election", 'pos'),
    ("Egypt Airlines crashed", 'neg'),
    ('I liked the movie we saw yesterday', 'pos'),
]

cl = NaiveBayesClassifier(train)

# Compute accuracy
def accuracy():
	acc = cl.accuracy(test)
	#print("Accuracy: {0}".format(cl.accuracy(test)))
	return acc

cl_accuracy = accuracy()
print (cl_accuracy)
