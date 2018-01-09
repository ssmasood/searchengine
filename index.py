import os
from bs4 import BeautifulSoup
import collections
from math import log10
from nltk.corpus import stopwords
import csv
import re
cachedStopWords = stopwords.words("english")


def InvertedIndex ():
        #dictionary of inverted index for searching through. All values initialized as empty lists.
        word_index = collections.defaultdict(dict)
        word_count = collections.defaultdict(int)
        filenamecount = 0;
        filecount = 0;
        for filename in os.listdir('WEBPAGES_CLEAN/'):
                if '.' not in filename:
                        for file in os.listdir('WEBPAGES_CLEAN/' + filename):
                                f = open(('WEBPAGES_CLEAN/' + filename + '/' + file), "r")
                                soup = BeautifulSoup(f, 'html.parser')
                                
                                ''' replace all unnecessary elements in the text with whitespace, or just remove them '''
                                #page_string = soup.get_text().replace("\\"," ").replace("'", " ").replace('"','').replace("-"," ").replace(".","").replace("!","").replace("?","").replace(",","").replace(">"," ").replace("<"," ").replace(";"," ").replace(":"," ").replace("["," ").replace("]"," ").replace("{"," ").replace("}"," ").replace("_"," ").replace("="," ").replace("+"," ").replace("("," ").replace(")"," ").replace("*"," ").replace("&"," ").replace("^"," ").replace("%"," ").replace("$"," ").replace("#"," ").replace("@"," ").replace("~"," ").replace("|"," ").replace("/"," ")
                                ''' Add all words in page to a dict, and add the current file index as a value. Must check if duplicate not found in list first. '''
        
                                temp_count = 0
                                for word in re.findall('[A-z0-9]+', soup.get_text().lower()):
                                        temp_count += 1
                                        if word in word_index and word not in cachedStopWords:
                                                if (filename,file) in word_index[word]:
                                                        word_index[word][(filename,file)] += 1
                                                        
                                                else:
                                                        word_index[word][(filename,file)] = 1
                                        else:
                                                word_index[word][(filename,file)] = 1
                                word_count[(filename,file)] = temp_count
                                print(filename)
                                f.close()
        for word in word_index:
                for key, val in word_index[word].items():
                        word_index[word][key] = '{:.7f}'.format(round(val/float(word_count[key]), 7))
                        
        print(filecount)
        print(len(word_index))
        w = csv.writer(open("invertedIndex.csv", "w"))
        for key, val in word_index.items():
                w.writerow([key, val])
  


InvertedIndex()
