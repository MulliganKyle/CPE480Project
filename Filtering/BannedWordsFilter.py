# 10/21/16
# BannedWordsFilter.py
#
# TweetFilter implementation that filters tweets based on 

import os
from TweetFilter import *


class BannedWordsFilter(TweetFilter):
	"""
	folder: str
		Name of the folder containing banned words.
	wordList: list
		All banned words in the blacklist folder.
	"""

	def __init__(self): 
		self.folder = 'Filtering/blacklist'
		self.wordsList = set()

	def filter(self, tweets):
		toRemove = set()
		filteredTweets = set()

		full_filepath = os.path.abspath(self.folder)
		filenames = os.listdir(full_filepath)

		# Loop through every file in the blacklist folder.
		for filename in filenames:
			print 'Loading banned words from %s' %filename
			full_filename = os.path.join(full_filepath, filename)

			# For each string in the file, add a key to the set.
			with open(full_filename) as stream:
				lines = stream.read().splitlines()

			self.wordsList.update(lines)


		# print 'The following words were added to the banned words list: '
		# for word in self.wordsList:
		# 	 print word

		for tweet in tweets:
			if self.containsBannedWord(tweet.text):
				toRemove.add(tweet)

		for tweet in tweets:
			if tweet not in toRemove:
				filteredTweets.add(tweet)

		return filteredTweets

	def containsBannedWord(self, text):
		for token in text.split(' '):
			if token in self.wordsList: 
				# print '%s is a banned word' %token
				# print 'removing the following tweet: %s' %text
				return True

		return False
