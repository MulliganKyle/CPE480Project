# 10/21/2016
# Tweet.py
#
# Definition for a class that holds data for a single tweet from twitter.

from Memes.MemeClass import MemeType

class Tweet(object) :
	"""
	topic: str
		Twitter topic that was used in the query that found this tweet.
	text: str
		Main body of the tweet.
	memeClass: MemeType
		Meme that this tweet fits into
	memeTextUpper: str
		Top portion of the meme this tweet fits into
	memeTextLower: str
		Lower portion of the meme this tweet fits into
	image: obj
		Generated meme image
	"""

	def __init__(self, topic, text):
		self.topic = topic
		self.text = text
		self.memeClass = MemeType.UNKNOWN
		self.memeTextUpper = None
		self.memeTextLower = None
		self.image = None
