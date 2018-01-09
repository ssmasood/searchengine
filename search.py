import csv
import json
import sys
import re
import collections
from pprint import pprint
from math import log10
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")
totalDocCount = 37497
csv.field_size_limit(sys.maxsize)
words = {}
for key, val in csv.reader(open("invertedIndex.csv")):
    words[key] = val

with open('WEBPAGES_CLEAN/bookkeeping.json') as data_file:
    data = json.load(data_file)

def tfidf(word, ranking, document):
    global totalDocCount
    documentFrequency = len(ranking[word]) #The number of documents containing a particular term
    inverseDocumentFrequency = log10(totalDocCount/float(documentFrequency)) #Reflects how important a term is to a document in a collection/corpus.
    ''' gota change this line below '''
    termFrequency = ranking[word][document] #The number of times a term occurs in a document divided by total of words in that document
    termFrequency_inverseDocumentFrequency = log10(1+float(termFrequency))*float(inverseDocumentFrequency)
    return termFrequency_inverseDocumentFrequency

def search(word):
    
    global words
    global data
    file = open(word + ".txt", "w")
    word = ' '.join([a for a in word.split() if a not in cachedStopWords])
    urllist = collections.defaultdict(dict)
    ranking = collections.defaultdict(dict)
    rankedlist = collections.defaultdict(float)
    
    for word1 in word.split():
        lis = re.findall(r"\d*\.?\d+[eE]?[-+]?\d*", words[word1.lower()])
        #lis = re.findall(r"\d*\.?\d+", words[word1.lower()])
        for num in range(0, len(lis), 3):
            ranking[word1][(lis[num], lis[num+1])] = lis[num+2]
            
    for key, val in ranking.items():
        for key1, val1 in val.items():
            urllist[key][key1] = tfidf(key, ranking, key1)
            
    for word1 in word.split():
        for url, tfidff in urllist[word1].items():
            rankedlist[url] += float(tfidff)
    finallist = sorted(rankedlist, key=rankedlist.__getitem__, reverse=True)
    #for key, val in rankedlist.items():
    #    file.write(str(key) + ' + ' + str(val))
    if len(finallist) >= 20:
        for num in range(20):
            file.write(data[finallist[num][0] + '/' + finallist[num][1]] + '\n')
    else:
        for num in finallist:
            file.write(data[num[0] + '/' + num[1]] + '\n')
    file.close()

        
