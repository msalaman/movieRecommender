<<<<<<< HEAD
#!/usr/bin/env python
=======
#!/usr/bin/env python3
>>>>>>> 07fbd39eb1119e797d3228102bc2590d98d6b48f

'''
    main.py

    CSE 40437 Final Project
    Abby Lane, Marcos Salamanca, Jack Meyer

    Give movie rec(s) based on user's recent tweets
'''
from __future__ import division, unicode_literals
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
import random
import imp
import numpy


imp.reload(sys)
#sys.setdefaultencoding('utf-8')

# -*- coding: utf-8 -*-


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

    print("\nAnalyzing " + username + "'s tweets...")

    for status in Cursor(api.user_timeline, id=user.id).items():
        count = count + 1
        if count == 50:
            break

        sentiment = get_tweet_sentiment(status.text)
        userTweets[status.id] = [status.text, sentiment]

        # print(count, sentiment, status.text)

        if sentiment > max:
            max = sentiment
            maxTweet = status.text

    print("\nTweet with highest sentiment: ")
    print(" - Tweet: " + clean_tweet(maxTweet) )
    print(" - Sentiment: " + str(max))

    return maxTweet, max

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
    scores = []
    for word, score in sorted_words:
        words.append(word)
        scores.append(score)
        # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    #print(words)
    #get only stems of words
    porter = PorterStemmer()
    words = [porter.stem(word) for word in words]
    return words, scores

# 3. Take in words[], return corresponding genre, if no genre found then it returns empty string
def getGenre(words):
    print("\nAssigning genre from Tweet content...\n")
    # open genreKeywords.txt
    index = 0
    for word in words: #goes through list of words that have already been ordered by importance
        for genre, kws in genreDict.items(): #check word matches to any genre keyword
            for kw in kws:
                if word in kw: #word could be stem of keyword
                    # print('word:' + word + ' --> keyword:' + kw + ' --> genre:' + genre)
                    return genre, index
        index += 1
    return '', 0

# 4. Take in genre, return movie(s)
def getMovie(genre):
    movies = open("ml-latest-small/movies.csv", "r", encoding="utf8").read().splitlines()

    while True:
        # from movies.csv, select a random listing
        # if the genres match, return movie title
        # else continue until one is found
        movie = random.choice(movies)
        movieTitle = movie.split(",")[1]
        genres = (movie.split(","))[2]
        try:
            genreList = genres.split("|")
        except:
            genreList = genres

        if genre in genreList:
            return movieTitle
        else:
            continue

    return ''


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
print("\n-----------------------")
username = sys.argv[1] if len(sys.argv) > 1 else raw_input("Enter a Twitter username (eg: @johnsmith): \n-> ")

print("-----------------------")
positiveTweet, maxSentiment = getTweet(username)
words, scores = getWords(positiveTweet)
genre, index = getGenre(words)
if genre:
    print("****** Recommended genre: " + genre + " ******")

    movie = getMovie(genre)

    print("****** Movie: " + movie + " ******\n")
    #We validate the accuracy by taking the TD-IDF score of the word used divided by the max TD-IDF score found in the tweet and adding it to the sentiment score of the tweet. We then divide the sum by 2 to get a decimal score out of 1. 1 is most confident, 0 is most likely inaccurate.
    print("****** Accuracy: " + str((scores[index]/(numpy.max(scores)) + maxSentiment)/2) + "******\n")

    # test screen name = 'AbbyLan78016969'
else:
    print('Could not find genre')
