# playing with twitter data

import twitter
import json
import nltk
import re
import networkx as nx
import matplotlib.pyplot as plt

twitter_api = twitter.Twitter(domain = "api.twitter.com")

# twitter trends
WORLD_WOE_ID = 1
world_trends = twitter_api.trends._(WORLD_WOE_ID)
twitter_trends = world_trends()[0]['trends']

for trend in twitter_trends:
	print trend

# search results
# https://dev.twitter.com/docs/api/1/get/search
search_results = []
QUERY = 'obamacare'
NPAGES = 6
twitter_search = twitter.Twitter(domain = "search.twitter.com")
for page in range(1, NPAGES):
	search_results.append(twitter_search.search(q = QUERY, rpp = 100, page = page, result_type = 'recent', sort_keys = True, include_entities = True))

print json.dumps(search_results, indent = 1)

# place the 'text' field of the json search results into a list
tweets = [ r['text']
	for result in search_results
		for r in result['results']
]
for t in tweets:
	print t

# compute lexical diversity for the search results
words = []
for t in tweets:
	words += [ w for w in t.split() ]

total_words = len(words)
unique_words = len(set(words))

# lexical diversity = % of words that are unique
print (1.0 * unique_words / total_words)

# avg words per tweet
print (1.0 * sum( [ len(t.split()) for t in tweets]) / len(tweets))

# frequency distribution
freq_dist = nltk.FreqDist(words)
print "top 20:\n", freq_dist.keys()[:20]
print "bottom 20:\n", freq_dist.keys()[-20:]

# extracting usernames
#username_re = re.compile(r'([A-Za-z0-9_]+)')
from_usernames = [ r['from_user_name']
	for page in search_results
		for r in page['results']
]
for u in from_usernames:
	print u

to_usernames = [ r['to_user_name']
	for page in search_results
		for r in page['results']
]
for u in to_usernames:
	print u

# make network graph of those who tweet about the query
g = nx.DiGraph()

for page in search_results:
	for r in page['results']:
		g.add_edge(r['from_user_name'], r['to_user_name'], {"id": r['id']})

g.number_of_nodes()
# g.number_of_edges()
g.draw()
plt.show()

