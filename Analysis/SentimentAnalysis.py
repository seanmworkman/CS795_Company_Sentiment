import nltk
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from flask import Flask, json, request
import requests
import yfinance as yf

import os
import json
import pandas as polDict
import datetime
import dateutil.parser
import unicodedata
import time


nltk.download([
    "stopwords",
    "punkt",
    "vader_lexicon",
    "twitter_samples"
])




# nltk.download('twitter_samples')

# positive_tweets = twitter_samples.strings('positive_tweets.json')
# negative_tweets = twitter_samples.strings('negative_tweets.json')

emoticonMap = {}
sia = SentimentIntensityAnalyzer()

def auth():
    print('TOKEN:', os.getenv('TOKEN'))
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, max_results = 10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    query_params = {
        'query': keyword,
        'max_results': max_results
    }

    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def getEmoticonMap():
    f = open('EmoticonMapping.txt')
    emDict = {}
    for i in f:
        i = i.replace('\n', '')
        splitLine = i.split(',')
        emDict[splitLine[0].strip()] = splitLine[1].strip()

    return emDict

# Map the passed emoticon if exists in map, else return the original 
def mapEmoticon(emoticon):
    try:
        return emoticonMap[emoticon]
    except:
        return emoticon

# Run all tweets through preprocessing
def preprocessData(data):
    preprocessedData = []
    for i in range(len(data)):
        tweet = data[i]
        tweet = tweet.replace('.', '')
        tweet = tweet.replace('\n', '')
        tweet = tweet.replace('"', '')
        tweet = tweet.replace('#', '')
        splitTweet = tweet.split(' ')
        # Remove stop words
        splitTweet = [word for word in splitTweet if not word.lower() in stopwords.words()]
        # Map emoticons
        for k in range(len(splitTweet)):
            if 'http' in splitTweet[k] or '@' in splitTweet[k]:
                splitTweet[k] = ''
            if '🚀' in splitTweet[k]:
                splitTweet[k] = 'great'
            if '🙏' in splitTweet[k]:
                splitTweet[k] = 'hopeful'

            splitTweet[k] = mapEmoticon(splitTweet[k])

        tweet = ' '.join(splitTweet)
        tweet = tweet.replace(';', '')
        tweet = tweet.replace('!', '')
        tweet = tweet.replace(':', '')
        if len(tweet) == 0:
            continue
        preprocessedData.append(tweet)

    return preprocessedData

def polarity(neg, neu, pos):
    maxi = max(neg, neu, pos)
    if maxi == neg:
        return -1
    if maxi == neu:
        return 0
    if maxi == pos:
        return 1

# 0
def unigramSentiment(data):
    processedData = preprocessData(data)

    aggregateSentiment = []

    for i in processedData:
        tweet = i.split(' ')
        polList = []
        polOfTweet = 0
        for k in tweet:
            polDict = sia.polarity_scores(k)
            polList.append(polarity(polDict['neg'], polDict['neu'], polDict['pos']))
        
        if len(polList) == 0:
            continue

        polOfTweet = sum(polList) / len(polList)

        aggregateSentiment.append(polOfTweet)

    return sum(aggregateSentiment) / len(aggregateSentiment)

# 1
def bigramSentiment(data):
    processedData = preprocessData(data)

    aggregateSentiment = []

    for i in processedData:
        nltk_tokens = nltk.word_tokenize(i)  	

        bigramList = list(nltk.bigrams(nltk_tokens))

        polList = []
        polOfTweet = 0
        for k in bigramList:
            tweet = " ".join(k)
            polDict = sia.polarity_scores(tweet)
            polList.append(polarity(polDict['neg'], polDict['neu'], polDict['pos']))

        if len(polList) == 0:
            continue

        polOfTweet = sum(polList) / len(polList)

        aggregateSentiment.append(polOfTweet)

    return sum(aggregateSentiment) / len(aggregateSentiment)

# 2
def preTrainedSentiment(data):
    processedData = preprocessData(data)

    aggregateSentiment = []

    for i in processedData:
        polDict = sia.polarity_scores(i)
        aggregateSentiment.append(polarity(polDict['neg'], polDict['neu'], polDict['pos']))

    return sum(aggregateSentiment) / len(aggregateSentiment)

def getCompanyFromTicker(ticker):
    company = ''
    try:
        company = yf.Ticker(ticker)
        return company.info['longName']
    except:
        return ''

def gatherData(searchTerm):
    # Connection to twitter API
    bearer_token = auth()
    headers = create_headers(bearer_token)
    max_results = 10

    data = []

    # Initial Search Term
    keyword = searchTerm + " lang:en"
    url = create_url(keyword, max_results)

    json_response = connect_to_endpoint(url[0], headers, url[1])

    for i in json_response['data']:
        data.append(i['text'])

    compFromTicker = getCompanyFromTicker(searchTerm) 
    if not compFromTicker == '' and not compFromTicker == None:
        # Search both ticker and company on Twitter
        keyword = compFromTicker + " lang:en"
        url = create_url(keyword, max_results)

        json_response = connect_to_endpoint(url[0], headers, url[1])

        for i in json_response['data']:
            data.append(i['text'])

    return data


def runAnalysis(method, searchTerm):
    data = gatherData(searchTerm)
    if method == 0: return unigramSentiment(data)
    if method == 1: return bigramSentiment(data)
    if method == 2: return preTrainedSentiment(data)
    else: return 0.0


emoticonMap = getEmoticonMap()
# api = Flask(__name__)

# @api.route('/sentAnalysis', methods=['GET'])
# def get_message():
#     output = runAnalysis(int(request.args['method']), request.args['searchTerm'])
#     return str(output)

# if __name__ == '__main__':
#     api.run(debug=True,host='0.0.0.0',port=5000)

print(runAnalysis(0, "AMC"))

# http://127.0.0.1:5000/sentAnalysis?method=0&searchTerm=AAPL





