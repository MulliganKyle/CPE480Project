# 10/21/16
# TweetFilter.py
#
# Abstract class that defines required behavior for a class that filters tweets.

import sys
sys.path.insert(0, '../Twitter API')

from Tweet import *

class TweetFilter(object) :

	# Takes in a list of tweets and returns a list whose size has been reduced using some filtering criteria
	def filter (self, tweets) :
		raise NotImplementedError("This class must implement the filter(tweets) method")