import copy

from Filtering.BannedWordsFilter import BannedWordsFilter
from Filtering.RandomFilter import RandomFilter
from Twitter.Tweet import Tweet
from Memes.MemeClass import *
from MemeGen.memegenerator import make_meme


def bid_on_tweet(memes, tweet):
   max_score = 0

   tweet = copy.deepcopy(tweet)
   for meme_obj in memes:
      text, score = meme_obj.generate(tweet)
      if score > max_score:
         max_score = score
         words = text.split(' ')
         split = len(words) / 2

         tweet.meme_text_upper = ' '.join(words[:split])
         tweet.meme_text_lower = ' '.join(words[split:])
         tweet.meme_class = meme_obj

   return tweet


def generator():
   # Get tweets.
   dump = open("Twitter/Dumps/SerializedTweets.p", "rb")
   tweets = pickle.load(dump)

   # Get single tweet.
   banned_filter = BannedWordsFilter()
   filtered_tweets = banned_filter.filter(tweets)
   random_filter = RandomFilter(1)
   tweet = random_filter.filter(filtered_tweets)[0]

   # Initialize MemeClasses.
   memes = [Meme_Doge('standard.jpg', score=0.1),
            Meme_XAllTheY('standard.jpg',score=0.2),
            Meme_OneDoesNotSimply('standard.jpg', score=0.2),
            Meme_JackieChan('standard.jpg', score=0.2,
                            classifier='temp.pickle', func=None)]

   # Gets the best matching meme and makes a meme for it.
   tweet = bid_on_tweet(memes, tweet)
   tweet.image = make_meme(tweet.meme_text_upper,
                           tweet.meme_text_lower,
                           tweet.meme_class.filename)
   tweet.image.save("Meme.png")
   

if __name__ == "__main__":
   generator()
