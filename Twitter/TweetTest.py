import unittest
from Tweet import *
from Memes.MemeClass import MemeType


class TweetTest(unittest.TestCase):

   def test_default(self):
      tweet1 = Tweet('topic1', 'text1')
      self.assertEquals(tweet1.memeClass, MemeType.UNKNOWN)

   def test_update(self):
      tweet1 = Tweet('topic1', 'text1')
      tweet1.memeClass = MemeType.KERMIT
      self.assertEquals(tweet1.memeClass, MemeType.KERMIT)


if __name__ == '__main__':
    unittest.main()
