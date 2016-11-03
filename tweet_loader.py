from __future__ import print_function
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
NUM_OF_TWEETS_CUSTOM = 100


def rate_limit_status():
	data = api.rate_limit_status()
	print("Rate Limit Status:\n")
	print("Trends: " + str(data['resources']['trends']['/trends/place']))
	print("Searches: " + str(data['resources']['search']['/search/tweets']))

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
		dumpTextFile.write("--------------------------------------------------------------------------------------------------------------------------------------------\n")
		dumpTextFile.write("Topic: " + tweet.topic + "\nTweet(s):\n")
		dumpTextFile.write(tweet.text.encode('utf8') + "\n")
		dumpTextFile.write("--------------------------------------------------------------------------------------------------------------------------------------------\n")

def scrub_tweet(tweet):
	# Take out RT's
	if tweet.text[:3] == 'RT ':
		tweet.text = tweet.text[3:]
	# Take out hyper links
	tweet.text = re.sub(r"http\S+", "", tweet.text)

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
			print("Pre-scrub:\n" + new_tweet_object.text + "\n")
			scrub_tweet(new_tweet_object)
			print("Post-scrub:\n" + new_tweet_object.text + "\n")
			tweets_to_analyze.add(new_tweet_object)
	return tweets_to_analyze

def custom_dump(desiredTopic): 
	print("inside custom_dump")
	tweets_to_analyze = set()
	searches = searches_left()
	count = 0

	while (searches > 1):

		#get NUM_OF_TWEETS tweets per trendName (max 100)
		tweets = tweepy.Cursor(api.search, q = desiredTopic).items(NUM_OF_TWEETS_CUSTOM)

		for tweet in tweets:
			count += 1
			new_tweet_object = Tweet(desiredTopic, tweet.text.translate(non_bmp_map))
			#print("Pre-scrub:\n" + new_tweet_object.text + "\n")
			scrub_tweet(new_tweet_object)
			#print("Post-scrub:\n" + new_tweet_object.text + "\n")
			tweets_to_analyze.add(new_tweet_object)

		print("got " + str(count) + " tweets")
		count = 0

		searches = searches_left()
		print("searches remaining: " + str(searches))

	return tweets_to_analyze

# Main entry point for the program
def loader():
	print('Inside tweet_loader.py')
	isCustomDump = False
	desiredTopic = ''
	dumpFileName = ''

	if len(sys.argv) == 3 :
		desiredTopic = sys.argv[1]
		dumpFileName = sys.argv[2]
		print(isCustomDump)
		isCustomDump = True
		print(isCustomDump)

		print("Performing custom twitter dump for topic: " + desiredTopic)

	else :
		print("Performing top-tweets dump")

	#print rate limit status
	rate_limit_status()
	
	#Check rate limit
	check_limit()

	#Pull tweets
	if(isCustomDump == True):
		serialized_tweets = custom_dump(desiredTopic)

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