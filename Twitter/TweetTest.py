import unittest
from Tweet import *
from Memes.MemeClass import *


class TweetTest(unittest.TestCase):

   def test_update(self):
      tweet = Tweet('topic1', 'this is my name')
      meme = Meme_Doge('temp.jpg', score=0.2)
      text, score = meme.generate(tweet)

      self.assertEquals(text, 'this is my name')
      self.assertEquals(score, 0.2)


if __name__ == '__main__':
    unittest.main()
