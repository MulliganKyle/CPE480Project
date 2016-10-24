import sys

import tweepy
from tweepy import OAuthHandler

from apiKeys import * #consumer_key, consumer_secret, access_token, and access_secret

united_states_woeid = 23424977

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

print ("RATE LIMIT AT START:")
data = api.rate_limit_status()
print ("Trends: " + str(data['resources']['trends']['/trends/place']))
print ("Searches: " + str(data['resources']['search']['/search/tweets']))
print ()

#trends_place returns the top 50 trending topics, if available
trends = api.trends_place(united_states_woeid)[0]['trends']
trendNames = [trend['name'] for trend in trends]

print("Here are the top " + str(len(trendNames)) + " trending topics in the United States:")
print(trendNames)

print("\nPrinting one tweet per topic")
for trendName in trendNames :

        #get 1 tweet per trendName (max 100)
        tweets = tweepy.Cursor(api.search, q = trendName).items(1)
        for tweet in tweets :
                print(tweet.text.translate(non_bmp_map) + "\n\n")


print ("\nRATE LIMIT AT END:")
data = api.rate_limit_status()
print ("Trends: " + str(data['resources']['trends']['/trends/place']))
print ("Searches: " + str(data['resources']['search']['/search/tweets']))
print ()
