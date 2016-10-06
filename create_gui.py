'''Create a HTML PAge from the Outputs'''
from bs4 import BeautifulSoup
from importlib import reload
import mainfile
reload(mainfile)
from mainfile import query, query_location, dictionary, sentiment_location, wc_location, hashtag_graph, url_sentiment

doc = '''
<html><head><title>Sentiment Analysis</title></head>
<body>
    <div id="container" style="border:thin">
    	<div id=tweetsentiment">
    		<h5>Tweet Sentiment</h5>
    	</div>
        <img src="./output/sentiment.png" alt="" height="250" width="250" />
    	<div id=Word Cloud">
    		<h5>Word Cloud</h5>
    	</div>
        <img src="./output/wc.png" alt="" height="250" width="250" />
	<div id=hashtag">
    		<h5>Hashtag Count</h5>
    	</div>
        <img src="./output/hashtag.png" alt="" height="250" width="250" />
    </div>
<table>
</table>
</body>
</html>
'''
soup = BeautifulSoup(doc,'html.parser')
body = soup.new_tag('body')
soup.insert(0, body)
table = soup.new_tag('table')
body.insert(0, table)


with open("./output/url_sentiment.txt") as infile:
    for line in infile:
        row = soup.new_tag('tr')
        col1, col2, col3 = line.split()
        for coltext in (col3, col2, col1): # important that you reverse order
            col = soup.new_tag('td')
            col.string = coltext
            row.insert(0, col)
        table.insert(len(table.contents), row)

with open('sentiment.html', 'w') as outfile:
    outfile.write(soup.prettify())
