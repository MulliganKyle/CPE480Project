'''
generate_hashtag.py generate
features for and construct
the hashtag classifier.

Note: Still room to refine features.
Implement UI to prompt for which hashtag
to train on as well as it's complementing
hashtag/emotion w/e

'''

import re
import pickle
from Twitter.Tweet import *

PATH = "Twitter/Dumps/SerializedTweets.p"

def generate_features():
   return


def clean_tweets(tweets):
# Remove hashtags, @'s, emojis
   for tweet in tweets:
       print("Pre-scrub: " + tweet.text)
       tweet.text = ' '.join(word for word in tweet.text.split(' ')
                                  if not word.startswith('#') and not word.startswith('@'))
       print("Post-scrub: " + tweet.text)


def main():
# Prompt user for what to train on...

# Ex: confused
# Unpickle tweets
   dump = open(PATH, "rb")

   # Load multiple dumps
   # #waitwhat, #unambiguous, #justdoit
   tweets = pickle.load(dump)

# Scrub tweets
   clean_tweets(tweets)

# Extract features (words)

# Throw tweet through classifiers


if __name__ == '__main__':
    main()
