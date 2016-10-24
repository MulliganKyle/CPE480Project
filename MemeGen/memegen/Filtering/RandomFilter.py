# 10/22/16
# RandomFilter.py
#
# TweetFilter implementation that returns a number of random tweets

import random
from TweetFilter import *

class RandomFilter (TweetFilter) :

	# Attributes:
	#	num: the number of tweets to select
	def __init__ (self, num) :
		self.num = num

	def filter (self, tweets) :

		randomTweets = set()

		if (self.num < 0) :
			return randomTweets
		elif (self.num <= len(tweets)) :
			return random.sample(tweets, self.num)
		else :
			return random.sample(tweets, len(tweets))