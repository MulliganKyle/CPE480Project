# 10/21/2016
# Tweet.py
#
# Definition for a class that holds data for a single tweet from twitter.

class Tweet(object) :
	"""
	topic: str
		Twitter topic that was used in the query that found this tweet.
	text: str
		Main body of the tweet.
	meme_class: obj
		Meme object that this tweet fits into
	meme_text_upper: str
		Top portion of the meme this tweet fits into
	meme_text_lower: str
		Lower portion of the meme this tweet fits into
	image: obj
		Generated meme image
	"""

	def __init__(self, topic, text):
		self.topic = topic
		self.text = text
		self.meme_class = None
		self.meme_text_upper = None
		self.meme_text_lower = None
		self.image = None
