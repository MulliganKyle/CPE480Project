'''
Make new twitter dummy acct
Check rate limit. on remaining trends, queries, searches 
Print tweets to file.
Scrub file. 
'''
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

def TimeDelay(timeToWait):
	time.sleep(timeToWait)

# If remaining is 1 or 15 wait 15mins. Running once a day? every 12 hours?
def CheckLimit():
	data = api.rate_limit_status()
	trendsRemaining = data['resources']['trends']['/trends/place']['remaining']
	searchesRemaining = data['resources']['search']['/search/tweets']['remaining']
	if trendsRemaining == 1 or searchesRemaining == 50:
		print "Exhausted limit...Waiting 15 mins.\n"
		TimeDelay(WAIT_TIME)

if __name__ == "__main__":
	while True:
		#Check rate limit
		CheckLimit()
		#IF it's fine, dump tweets

		#wait 24 hours
		TimeDelay(DAILY_TIME)