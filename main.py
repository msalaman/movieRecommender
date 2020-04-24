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
    user = api.get_user(screen_name=username)
    userTweets = {} #Tweet dictionary for user, key = tweetId; value[0] = tweetText' value[1] = sentiment

    max = -1
    maxTweet = ''

    for status in Cursor(api.user_timeline, id=user.id).items():
        sentiment = get_tweet_sentiment(status.text)
        userTweets[status.id] = [status.text, sentiment]
        if sentiment > max:
            max = sentiment
            maxTweet = status.text

    # for i in userTweets:
    #     print(i, userTweets[i])
        print("Tweet: " + maxTweet )
        print("Sentiment: " + str(sentiment))

        return maxTweet

# 2. Take in a tweet, return the most important words
def getWords(tweet):
    words = []
    return words

# 3. Take in words[], return corresponding genre
def getGenre(words):
    # open genreKeywords.txt
    # open tags.txt
    genre = ''
    return genre

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
print("USERNAME: " + username)
positiveTweet = getTweet(username)
# test screen name = 'AbbyLan78016969'
