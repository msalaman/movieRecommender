#!/usr/bin/env python

'''
    main.py

    CSE 40437 Final Project
    Abby Lane, Marcos Salamanca, Jack Meyer

    Give movie rec(s) based on user's recent tweets
'''
import tweepy, json
import sys, os, re
from textblob import TextBlob
from tweepy import Cursor, OAuthHandler, Stream, StreamListener
from six.moves import input as raw_input
import nltk
nltk.download('gutenberg')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import gutenberg
import math
import ast
from genreKeywords import genreDict

#TF-IDF functions from https://stevenloria.com/tf-idf/
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

#Source for sentiment analysis https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # return sentiment score
    return analysis.sentiment.polarity

# 1. Take in user, return most positive tweet(s)
def getTweet(username):
    try:
        user = api.get_user(screen_name=username)
    except:
        print("Error: \"" + username + "\" is not a valid twitter username")
        return -1

    userTweets = {} #Tweet dictionary for user, key = tweetId; value[0] = tweetText' value[1] = sentiment

    max = -1
    maxTweet = ''
    count = 0 # only look at past 50 tweets

    print("\nAnalyzing " + username + "'s tweets...'")

    for status in Cursor(api.user_timeline, id=user.id).items():
        count = count + 1
        if count == 50:
            break

        sentiment = get_tweet_sentiment(status.text)
        userTweets[status.id] = [status.text, sentiment]

        if sentiment > max:
            max = sentiment
            maxTweet = status.text

    print("\nTweet: " + maxTweet )
    print("Sentiment: " + str(max))

    return maxTweet

# 2. Take in a tweet, return the most important words
def getWords(tweet):
    #words = positiveTweet.split()
    blob = TextBlob(tweet)
    bloblist = []
    #using corpus text to compare our tweet to common English in order to calculate significane of words
    #Source: https://www.nltk.org/book/ch02.html
    for fileid in gutenberg.fileids()[:5]:
        bloblist.append(TextBlob(gutenberg.raw(fileid)))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    words = []
    for word, score in sorted_words:
        words.append(word)
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    print(words)
    #get only stems of words
    porter = PorterStemmer()
    words = [porter.stem(word) for word in words]
    return words

# 3. Take in words[], return corresponding genre, if no genre found then it returns empty string
def getGenre(words):
    # open genreKeywords.txt
    for word in words: #goes through list of words that have already been ordered by importance
        for genre, kws in genreDict.items(): #check word matches to any genre keyword
            for kw in kws:
                if word in kw: #word could be stem of keyword
                    print('word:' + word + ' --> keyword:' + kw + ' --> genre:' + genre)
                    return genre
    return ''

# 4. Take in genre, return movieID(s)
def getMovieID(genre):
    movie = ''
    return movie

# 5. Take in movieID, return movie title
def getMovie(ID):
    movie = ''
    # open 'ml-latest-small/movies.csv'
    return movie


''' Twitter token info '''

ACCESS_TOKEN = "1221578987870326785-oxOKp2lkUcFTidYhDfwdsjwbOOcDF0"
ACCESS_TOKEN_SECRET = "6e9lRkqxlMuotKcohvvB7s4oEpo5gBkIAKMkQqzKZnrsc"
CONSUMER_KEY = "OsHAeLLTINOFA9uhor0KLnGeh"
CONSUMER_SECRET = "0mr25tTCYPlSxKufS6qqgQprHviKxeKhgPfTLrSgsHfAdOh6BK"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
myStreamListener = StreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

username = raw_input("Enter a Twitter username (eg: @johnsmith): ")
print("\nUsername: " + username)
positiveTweet = getTweet(username)
words = getWords(positiveTweet)
getGenre(words)

# test screen name = 'AbbyLan78016969'
