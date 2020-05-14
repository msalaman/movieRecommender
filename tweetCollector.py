#!/usr/bin/env python

import sys
import os
import tweepy
import re
from textblob import TextBlob
from tweepy import Cursor, OAuthHandler, Stream, StreamListener

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

'''For this program to work, you must insert your own twitter api credentials in your own local repository (Do not push your credentials to this public repository'''
ACCESS_TOKEN = '''Your Access Token'''
ACCESS_TOKEN_SECRET = '''Your Access Token Secret'''
CONSUMER_KEY = '''Your Consumer Key'''
CONSUMER_SECRET = '''Your Consumer Secret'''


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
myStreamListener = StreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)


user = api.get_user(screen_name='AbbyLan78016969')
userTweets = {} #Tweet dictionary for user, key = tweetId; value[0] = tweetText' value[1] = sentiment
for status in Cursor(api.user_timeline, id=user.id).items():
    userTweets[status.id] = [status.text, get_tweet_sentiment(status.text)]

print(userTweets)
