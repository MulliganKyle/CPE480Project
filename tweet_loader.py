from __future__ import print_function
import os
import time
import sys
import tweepy
import re
import pickle
from tweepy import OAuthHandler
from config import * #consumer_key, consumer_secret, access_token, and access_secret
from Twitter.Tweet import *


# Authentication
united_states_woeid = 23424977
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
EXHAUST_TIME = 900 #15 mins
DAILY_TIME = 86400 #24 hours
NUM_OF_TWEETS = 1 #Per trending topic


def rate_limit_status():
	data = api.rate_limit_status()
	
	print("\nRate Limit Status:")
	print("Trends: " + str(data['resources']['trends']['/trends/place']))
	print("Searches: " + str(data['resources']['search']['/search/tweets']))
	print()


def searches_left():
	data = api.rate_limit_status()
	return data['resources']['search']['/search/tweets']['remaining']


def time_delay(timeToWait):
	time.sleep(timeToWait)


# If remaining is 1 or 15 wait 15mins. Running once a day? every 12 hours?
def check_limit():
	data = api.rate_limit_status()
	trendsRemaining = data['resources']['trends']['/trends/place']['remaining']
	searchesRemaining = data['resources']['search']['/search/tweets']['remaining']
	if trendsRemaining == 1 or searchesRemaining == 50:
		print("Exhausted limit...Waiting 15 mins.\n")
		TimeDelay(WAIT_TIME)


def dump_tweets(serialized_tweets, dumpFileName):

	dumpTextFile = open('Twitter/Dumps/' + dumpFileName + '.txt', 'a') #Append to dump file
	dumpPickleFileName = 'Twitter/Dumps/' + dumpFileName + '.p'

	pickle.dump(serialized_tweets, open(dumpPickleFileName, "wb" ))
	for tweet in serialized_tweets:
		dumpTextFile.write("[" + tweet + "]\n")


def scrub_tweet(tweet):
	# Take out RT's
	if tweet.text[:3] == 'RT ':
		tweet.text = tweet.text[3:]
	
	# Take out hyper links
	tweet.text = re.sub(r"http\S+", "", tweet.text) #removes URLs
	tweet.text = re.sub(r"#\S+", "", tweet.text) #removes hashtags
	tweet.text = re.sub(r'[^\x00-\x7F]+', '', tweet.text) #removes non-ASCII chars
	tweet.text = re.sub(r"@\S+: ", "", tweet.text) #removes tweet author
	tweet.text = re.sub(r"&amp;", "and", tweet.text) #replaces "&amp;" with "and"
	tweet.text = tweet.text.strip() #removes leading and trailing whitespace


#Accesses the top trending topics from twitter and pulls NUM_OF_TWEETS tweets
def top_tweets_dump():
	tweets_to_analyze = set()

	#trends_place returns the top 50 trending topics, if available
	trends = api.trends_place(united_states_woeid)[0]['trends']
	trendNames = [trend['name'] for trend in trends]
	print(trendNames)
	return tweets_to_analyze

	for trendName in trendNames:

		#get NUM_OF_TWEETS tweets per trendName (max 100)
		tweets = tweepy.Cursor(api.search, q = trendName).items(NUM_OF_TWEETS)
		for tweet in tweets:
			new_tweet_object = Tweet(trendName, tweet.text.translate(non_bmp_map))
			scrub_tweet(new_tweet_object)
			tweets_to_analyze.add(new_tweet_object)
	return tweets_to_analyze

def custom_dump(desiredTopic, desiredTweetCount):
	print("Performing custom twitter dump for the following topic: " + desiredTopic)
	
	tweets_to_analyze = set()
	searches = searches_left()
	count = 0
	duplicates = 0

	print("Requesting " + str(desiredTweetCount) + " tweets with topic " + desiredTopic)
	sys.stdout.flush()
	tweets = tweepy.Cursor(api.search, q = desiredTopic).items(desiredTweetCount)

	for tweet in tweets:
		count += 1
		new_tweet_object = Tweet(desiredTopic, tweet.text.translate(non_bmp_map))
		scrub_tweet(new_tweet_object)
		
		size = len(tweets_to_analyze)
		tweets_to_analyze.add(new_tweet_object.text)

		if size == len(tweets_to_analyze):
			duplicates += 1

	print("Got " + str(count) + " tweets, with " + str(duplicates) + " duplicates")
	print("Total number of tweets retrieved: " + str(len(tweets_to_analyze)))
	sys.stdout.flush()
	count = 0
	duplicates = 0

	searches = searches_left()
	print(str(searches) + " searches left")

	return tweets_to_analyze


# Main entry point for the program
def loader():
	print('Inside tweet_loader.py')
	isCustomDump = False
	desiredTopic = ''
	dumpFileName = ''
	desiredTweetCount = 0

	if len(sys.argv) == 4:
		desiredTopic = sys.argv[1]
		dumpFileName = sys.argv[2]
		desiredTweetCount = int(sys.argv[3])
		isCustomDump = True

	#print rate limit status
	rate_limit_status()

	#Check rate limit
	check_limit()

	#Pull tweets
	if(isCustomDump == True):
		serialized_tweets = custom_dump(desiredTopic, desiredTweetCount)

		#Dump tweets
		dump_tweets(serialized_tweets, dumpFileName)

	else:
		serialized_tweets = top_tweets_dump()

		#Dump tweets
		dump_tweets(serialized_tweets, "SerializedTweets")

	#Rate limit status
	rate_limit_status()

	#wait 24 hours


if __name__ == "__main__":
   loader()
