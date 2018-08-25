#!/bin/python

import requests
import json
import os
import re
import pickle
import pprint
import string
import unicodedata
import logging
pp = pprint.PrettyPrinter(indent=4)

class NewsScraper:
    def __init__(self):
        self.parse_arguments()
        self.CHANNEL_FILE = "../etc/all.txt"
        self.totalArticles = 0  #Maintains a count of retrieved articles
        self.channelMap = {}
        self.urlTail = '&apiKey=f9fff49292124700b36b8ec86c76339a'
        self.articles = {}
        self.articleDumpFile = '../data/articles.csv'
        self.pickleDumpPath = os.path.join('..', 'etc', 'pkcl')
        FORMAT = '%(asctime)-15s %(filename)s %(funcName)s:%(lineno)d %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('tcpserver')
        # self.logger.setLevel(logging.DEBUG)
        self.logger.info('News Collector initiated.')

    def parse_arguments(self):
        pass

    def prepareGrammar(self):
        emoticons_str = r"""
            (?:
                [:=;] # Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""

        regex_str = [
            r'<[^>]+>', # HTML tags
            r"(?:[a-z][a-z\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
        ]

        print ("Defining grammar..")
        self.tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


    def processString(self, data):
        '''
            Process string to remove punctuation
        '''
        if not data:
            return ''
        data = data.strip().lower()
        self.logger.debug("Processing the String: "+ data)
        data = unicodedata.normalize('NFKD', data)
        data = data.encode('utf-8','backslashreplace')
        return data.translate(None, string.punctuation)

    def dumpArticles(self, jsonArticles):
        '''
            Dumps Articles from JSON to a csv File
        '''
        self.totalArticles += len(jsonArticles)
        if not os.path.isfile(self.articleDumpFile):
            with open(self.articleDumpFile, 'w') as f:
                f.write('TITLE,DESCRIPTION,AUTHOR,SOURCE,URL,RATING\n')

        with open(self.articleDumpFile, 'a') as f:
            for lArticle in jsonArticles:
                self.logger.debug('Article being Processed: ' + str(lArticle))
                csvString = self.processString(lArticle.get('title', '')) + ','
                csvString += self.processString(lArticle.get('description', '')) + ','
                csvString += self.processString(lArticle.get('author', '')) + ','
                csvString += self.processString(lArticle.get('source', '').get('name','')) + ','
                self.logger.debug('URL: ' + lArticle.get('url', ''))
                csvString += str(lArticle.get('url','').encode('utf-8','backslashreplace')) + ',\n'
                self.logger.debug('CSV String: ' + csvString)
                f.write(csvString)

    def createChannelMap(self):
        '''
            Creates a map of channel names and channel codes from CHANNEL_FILE
        '''
        self.logger.info("Preparing Channel Map")
        f = open(self.CHANNEL_FILE)
        channels = f.readlines()
        f.close()
        for i in range(0, len(channels), 2):
            cName = channels[i].strip()
            cId = channels[i+1].strip()
            self.channelMap[cName] = cId
        self.logger.info("Prepared Channel Map")

    def retrieveArticles(self, url, pickleFile=None):
        '''
            Retrieves news articles from the URL and dumps them if file is passed
        '''
        self.logger.debug('Retrieving info from ' + url)
        response = requests.get(url)
        jsonData = json.loads(json.dumps(response.json()))
        if str(jsonData['status']).lower() == "ok":
            return jsonData
        self.logger.warning('Bad response from ' + url)
        return None

    def getNewsArticles(self, urlHead):
        '''
            Retrieves and dumps news articles
        '''
        for _, source in self.channelMap.items():
            self.logger.info('Scraping data from :' + source.upper())
            pickleFile = os.path.join(self.pickleDumpPath , source + '.pkcl')

            if not os.path.isfile(pickleFile):
                url = urlHead + source + self.urlTail
                self.logger.info('Dumping info from URL: ' + url + ' on to the file ' + pickleFile)
                jsonData = self.retrieveArticles(url, pickleFile)
                if not jsonData:    # Error Request
                    continue
                pickle.dump(jsonData['articles'], open(pickleFile,'w'))
                self.dumpArticles(jsonData.get('articles', []))
            else:
                self.logger.info("Loading from previous pickle file")
                with open(pickleFile) as f:
                    data = pickle.load(f)
                    self.dumpArticles(data)

    def initiateProcess(self):
        self.createChannelMap()
        self.getNewsArticles("https://newsapi.org/v2/top-headlines?sources=")
        print("Articles Retrieved: " + str(self.totalArticles))

if __name__ == "__main__":
    n = NewsScraper()
    n.initiateProcess()

