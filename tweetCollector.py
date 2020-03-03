#!/usr/bin/env python

import sys
import os
import tweepy
from tweepy import Cursor, OAuthHandler, Stream, StreamListener

ACCESS_TOKEN = "273162409-xV3a7cpTrY1t9hPV9ezQwKUDLLr5EceZnoekCtJD"
ACCESS_TOKEN_SECRET = "wEjcpSCeWKsWArOInus2GPImi7a7IsSlsZi4luKVfeMPe"
CONSUMER_KEY = "VZ0Ja4ITAt217GxgiBqct1ly5"
CONSUMER_SECRET = "OViM1vaFLR0n9qYZXGaaNlnhsC9KDmeIYuJRB4IV2bMX6xFTBm"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
myStreamListener = StreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)


user = api.get_user(screen_name='AbbyLan78016969')
userTweets = []
for status in Cursor(api.user_timeline, id=user.id).items():
    userTweets.append(status.text.split())

print(userTweets)

