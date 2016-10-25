from Filtering.BannedWordsFilter import BannedWordsFilter
from Filtering.RandomFilter import RandomFilter
from Twitter.Tweet import Tweet
from Memes.MemeClass import *


def bid_on_tweet(memes, tweet):
   max_score = 0
   tweet_text = ''

   for meme_obj in memes:
      text, score = meme_obj.generate(tweet)
      if score > max_score:
         max_score = score
         tweet_text = text

   print(score)
   return tweet_text



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
   memes = [Meme_Doge(0.1),
            Meme_XAllTheY(0.2),
            Meme_OneDoesNotSimply(0.2)]

   meme = bid_on_tweet(memes, tweet)
   print(meme)
   

if __name__ == "__main__":
   generator()
