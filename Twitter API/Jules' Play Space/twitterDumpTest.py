'''
Make new twitter dummy acct
Check rate limit. on remaining trends, queries, searches 
Print tweets to file.
Scrub file. 
'''
from __future__ import print_function
import time
import sys
import tweepy
from tweepy import OAuthHandler
from apiKeys import * #consumer_key, consumer_secret, access_token, and access_secret

# Authentication
united_states_woeid = 23424977
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
EXHAUST_TIME = 900 #15 mins
DAILY_TIME = 86400 #24 hours
NUM_OF_TWEETS = 1 #Per trending topic
dumpFile = open('Dump', 'a') #Append to dump file

def RateLimitStatus():
	data = api.rate_limit_status()
	print("Rate Limit Status:\n")
	print("Trends: " + str(data['resources']['trends']['/trends/place']))
	print("Searches: " + str(data['resources']['search']['/search/tweets']))

def TimeDelay(timeToWait):
	time.sleep(timeToWait)

# If remaining is 1 or 15 wait 15mins. Running once a day? every 12 hours?
def CheckLimit():
	data = api.rate_limit_status()
	trendsRemaining = data['resources']['trends']['/trends/place']['remaining']
	searchesRemaining = data['resources']['search']['/search/tweets']['remaining']
	if trendsRemaining == 1 or searchesRemaining == 50:
		print("Exhausted limit...Waiting 15 mins.\n")
		TimeDelay(WAIT_TIME)

def DumpTweets():
	trends = api.trends_place(united_states_woeid)[0]['trends']
	trendNames = [trend['name'] for trend in trends]
	dumpFile.write("Retrieved " + str(len(trendNames)) + " US trending topics:\n")
	dumpFile.write(str(trendNames))
	dumpFile.write("\nPrinting " + str(NUM_OF_TWEETS) + " tweet per topic\n")
	for trendName in trendNames:
		dumpFile.write("Topic: " + trendName.encode('utf8') + ". Tweet(s):\n")
  		#get 1 tweet per trendName (max 100)
   		tweets = tweepy.Cursor(api.search, q = trendName).items(NUM_OF_TWEETS)
   		for tweet in tweets:
   			dumpFile.write(tweet.text.translate(non_bmp_map).encode('utf8'))
   			dumpFile.write('\n\n')

if __name__ == "__main__":
	'''
	while True:
		#Rate limit status
		RateLimitStatus()
		#Check rate limit
		CheckLimit()
		#IF it's fine, dump tweets
		DumpTweets()
		#Rate limit status
		RateLimitStatus()
		#wait 24 hours
		TimeDelay(DAILY_TIME)
	'''
	#Rate limit status
	RateLimitStatus()
	#Check rate limit
	CheckLimit()
	#IF it's fine, dump tweets
	DumpTweets()
	#Rate limit status
	RateLimitStatus()
	#wait 24 hours
	TimeDelay(DAILY_TIME)