# 10/21/2016
# Tweet.py
# 
# Definition for a class that holds data for a single tweet from twitter.

import sys
sys.path.insert(0, '../Memes')

from MemeClass import MemeClass

class Tweet(object) :

	# Attributes:
	#	topic: A string representing the twitter topic that was used in the query that found this tweet
	#	text: A string containing the main body of the tweet
	#	memeClass: The meme that this tweet fits into
	#	memeTextUpper: The top portion of the meme this tweet fits into
	#	memeTextLower: The lower portion of the meme this tweet fits into
	#	image: The generated meme image

	def __init__ (self, topic, text) :
		self.topic = topic
		self.text = text
		self.memeClass = MemeClass.UNKNOWN
		self.memeTextUpper = ''
		self.memeTextLower = ''

