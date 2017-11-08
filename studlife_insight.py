import csv, sys, os, re, collections
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from bs4 import BeautifulSoup
from multiprocessing import Pool

def cleanContent(line):
	soup = BeautifulSoup(line[4], 'html.parser')

	# Strip tags
	stripped = soup.get_text()

	# Strip WP Shortcode
	stripped = re.sub(r'\[.*\]', '', stripped)

	# Strip extraneous newlines
	stripped = re.sub(r'\n+', '\n', stripped)

	line[4] = stripped

	return line

def analyzeSentiment(post):

	score = sentiment.polarity_scores(post[4])

	return post[4], score

def initPool():
    global sentiment
    sentiment = SentimentIntensityAnalyzer()

with open('../Downloads/testfile.csv') as corpus:
	file = csv.reader(corpus)
	scores = collections.OrderedDict()
	pool = Pool()
	cleaned = pool.map(cleanContent, file)

	# Remove attachments, post duplicates (keep only last revision)
	keep = []
	for record in cleaned:
		if len(record[4]) < 300 or record[21] == 'attachment':
			continue
		else:
			if record[18] == '0':
				keep.append(record[0])
			else:
				if record[18] in keep: keep.remove(record[18])
				keep.append(record[0])

	cleaned = {x: cleaned[x] for x in keep}

	for p in keep:
		print(p)

# 	pool = Pool(8, initPool, ())
# 	scores = pool.map(analyzeSentiment, cleaned_posts)

# sorted_scored = sorted(scores, key=lambda x:x[1]['neg'])

# for item in sorted_scored:
# 	print(item[0])
# 	print(item[1])
# 	print 

