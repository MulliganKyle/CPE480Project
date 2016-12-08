import copy
import tweepy
from tweepy import OAuthHandler
from random import shuffle

from Filtering.BannedWordsFilter import BannedWordsFilter
from Filtering.RandomFilter import RandomFilter

from MemeGen.memegenerator import make_meme
from Memes.classifiers.helpers import ClassifierType
import Memes.classifiers.generate_questions_classifier as gqc
import Memes.classifiers.generate_hashtag_classifier as ghc
import Memes.classifiers.generate_statements_classifier as gsc

from Memes.MemeClass import *
from Twitter.Tweet import Tweet
from config import *

MEME_IMG_FILENAME = 'Meme.png'
DEBUG = True

# Each meme bids on a tweet.
def bid_on_tweet(memes, tweet):
   map_scores = {}

   tweet = copy.deepcopy(tweet)
   for meme_obj in memes:
      text, score = meme_obj.generate(tweet.text)
      score = float(score)

      if score not in map_scores:
         map_scores[score] = []

      words = text.split(' ')
      split = len(words) / 2

      text_upper = ' '.join(words[:split])
      text_lower = ' '.join(words[split:])
      map_scores[score].append((text_upper, text_lower, meme_obj))

   key = sorted(map_scores, reverse=True)[0]
   tweets = map_scores[key]
   shuffle(tweets)

   tweet.meme_text_upper = tweets[0][0]
   tweet.meme_text_lower = tweets[0][1]
   tweet.meme_class = tweets[0][2]
   return tweet


def generator():
   # Get tweets.
   dump = open('Twitter/Dumps/waitwhat_new.p', 'rb')
   tweets = pickle.load(dump)

   # Get single tweet.
   banned_filter = BannedWordsFilter()
   filtered_tweets = banned_filter.filter(tweets)
   random_filter = RandomFilter(1)
   tweet_text = random_filter.filter(filtered_tweets)[0]

   # Initialize MemeClasses.
   memes = [Meme_Doge('doge.jpg', score=0.1),
            Meme_XAllTheY('x_all_the_y.jpg',score=0.2),
            Meme_OneDoesNotSimply('one_does_not_simply.jpg', score=0.2),
            Meme_JackieChan('jackie_chan.jpg',
                            classifier=ClassifierType.QUESTION,
                            func=gqc.generate_features),
            Meme_JackieChan_Hashtag('jackie_chan.jpg',
                            classifier=ClassifierType.HASHTAG,
                            func=ghc.generate_features)]
 #           Meme_Kermit('kermit.jpg',
 #                           classifier=ClassifierType.STATEMENT,
 #                           func=gsc.generate_features)]


   # Gets the best matching meme and makes a meme for it.
   tweet = Tweet(None, tweet_text)
   tweet = bid_on_tweet(memes, tweet)
   tweet.image = make_meme(tweet.meme_text_upper,
                           tweet.meme_text_lower,
                           tweet.meme_class.filename)
   tweet.image.save(MEME_IMG_FILENAME)

   # Print metadata about tweet.
   if DEBUG:
      print type(tweet.meme_class)
      print tweet.meme_text_upper
      print tweet.meme_text_lower

   # Posts tweet to Twitter.
   should_post = raw_input('Should I post to twitter? ')
   if should_post[0] == 'Y':
      print 'Posting to Twitter...'
      auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
      auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
      api = tweepy.API(auth)
      api.update_with_media(MEME_IMG_FILENAME, tweet.text)


if __name__ == "__main__":
   generator()
