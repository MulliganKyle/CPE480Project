import unittest

from BannedWordsFilter import *
from RandomFilter import *
from Twitter.Tweet import Tweet
from Memes.MemeClass import MemeType


class FilterTest(unittest.TestCase):

   def setUp(self):
      self.tweets = {Tweet('topic', 'body of tweet 1'),
                     Tweet('topic', 'Something offensive towards christians'),
                     Tweet('topic', 'body of tweet 2')}

   def test_banned_filter(self):
      tweet_filter = BannedWordsFilter()
      filtered_tweets = tweet_filter.filter(self.tweets)
      self.assertEquals(len(filtered_tweets), 2)

   def test_random_filter(self):
      tweet_filter = RandomFilter(1)
      filtered_tweets = tweet_filter.filter(self.tweets)
      self.assertEquals(len(filtered_tweets), 1)


if __name__ == '__main__':
    unittest.main()