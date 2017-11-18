import csv, sys, os, re, collections
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from bs4 import BeautifulSoup
from multiprocessing import Pool
import warnings

def cleanContent(line):
    
    # Filter bs4 URL warnings
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
        
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

def initSentimentPool():
    global sentiment
    sentiment = SentimentIntensityAnalyzer()

with open('./testfile.csv') as corpus:
    file = csv.reader(corpus)
    scores = collections.OrderedDict()
    
    print("Cleaning content...")
    
    # Clean post content
    pool = Pool()
    cleaned = pool.map(cleanContent, file)
    
    # Remove attachments, post duplicates (keep only last revision)
    
    ## Create dict of post_id : list of reivision_id's, in order
    
    print("Removing duplicates and non-text posts...")
    keep = {}
    for record in cleaned:
        if len(record[4]) < 300 or record[21] == 'attachment':
            continue
        else:
            if record[18] == '0':
                keep[int(record[0])] = [record[0]]
            else:
                if int(record[18]) in keep.keys():
                    keep[int(record[18])].append(int(record[0]))
                else:
                    keep[int(record[18])] = [record[18], record[0]]

    # Save last id of revision for each post
    keep = [value[-1] for key, value in keep.items()]
    
    # Filter csv data by these reivision id's
    cleaned = [x for x in cleaned if int(x[0]) in keep]
    
    print("Analyzing sentiment...")
    pool = Pool(8, initSentimentPool, ())
    scores = pool.map(analyzeSentiment, cleaned)

sorted_scored = sorted(scores, key=lambda x:x[1]['compound'])

for item in reversed(sorted_scored):
    print(item[0])
    print(item[1])
    print 

