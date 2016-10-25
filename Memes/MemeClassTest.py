import unittest
from Twitter.Tweet import *
from MemeClass import *


class TestMeme_XAllTheY(unittest.TestCase):

   def setUp(self):
      self.meme = Meme_OneDoesNotSimply(0.5)

   def test_generate(self):
      tweet = Tweet(topic='topic', text='@Sixers: The team has signed former Temple guard @Dchristmas22.')
      self.assertFalse()

   def test_update(self):
      pass


class TestMeme_OneDoesNotSimply(unittest.TestCase):

   def setUp(self):
      self.meme = Meme_OneDoesNotSimply(0.5)

   def test_generate_found(self):
      tweet = Tweet(topic='topic', text='I\'m old enough to remember   him.')
      text, score = self.meme.generate(tweet)
      self.assertEquals(text, 'One does not simply remember him.')
      self.assertEquals(score, 0.5)

   def test_generate_verb_apostrophe(self):
      tweet = Tweet(topic='topic', text='@potaytozayn: Retweet if you\'re a proud Swiftie')
      text, score = self.meme.generate(tweet)
      self.assertEquals(text, '')
      self.assertEquals(score, 0.0)

   def test_generate_small_verb(self):
      tweet = Tweet(topic='topic', text='This is a tweet')
      text, score = self.meme.generate(tweet)
      self.assertEquals(text, '')
      self.assertEquals(score, 0.0)

   def test_generate_no_verb(self):
      tweet = Tweet(topic='topic', text='Twitter yay happy.')
      text, score = self.meme.generate(tweet)
      self.assertEquals(text, '')
      self.assertEquals(score, 0.0)


if __name__ == '__main__':
    unittest.main()
