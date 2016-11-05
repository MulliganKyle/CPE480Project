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
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from Twitter.Tweet import *
from Memes.classifiers.helpers import *

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

#extrat single words as features from the training data
def generate_unigram_feature_list(training_data):
   return set(word.lower() for passage in training_data for word in word_tokenize(passage))

#extract bigrams as features form the training data
def generate_bigram_feature_list(training_data):
   features_bigrams = set()
   for sentence in training_data:
      for gram in ngrams(word_tokenize(sentence), 2):
         if gram not in features_bigrams:
            features_bigrams.add(gram)
   return features_bigrams


def generate_features(tweet, word_features, features_bigrams):
   training_set = []
   word_training_features = ({word: (word in word_tokenize(tweet)) for word in word_features})
   sentence_bigrams = []
   for gram in ngrams(word_tokenize(tweet), 2):
      if gram not in sentence_bigrams:
         sentence_bigrams.append(gram)
   bigram_training_features = ({word: (word in sentence_bigrams) for word in features_bigrams})
   #join all features unigram and bigram in one dict
   for key in word_training_features:
      bigram_training_features[key] = word_training_features[key]
   return bigram_training_features

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

# TODO: create lists with confused not confused tweets
   confused_tweets = []
   not_confused_tweets = []

   confused_tweets = [x.lower() for x in confused_tweets]
   not_confused_tweets = [x.lower() for x in not_confused_tweets]
   all_tweets = confused_tweets + not_confused_tweets   

   # Extract the features from the training data
   word_features = generate_unigram_feature_list(all_tweets)
   bigram_features = generate_bigram_feature_list(all_tweets)
# TODO:  This uses all "words" in the tweets as features.
#        Filter out punctuation and and specific word types as articles.

   # Generate features.
   data = []
   for confused in confused_tweets:
      data.append((generate_features(confused, word_features, bigram_features), True))
   for not_confused in not_confused_tweets:
      data.append((generate_features(not_confused, word_features, bigram_features), False))


   # Generates training and test set.
   training_data, test_data = split_training_test(data)

   # Generate classifier with score.
   classifier, score = create_classifier(training_data, test_data)
   print 'classifier score: %.4f' %score

   # Pickle classifier.
   pickle_classifier(classifier, score, ClassifierType.HASHTAG)



# Throw tweet through classifiers


if __name__ == '__main__':
    main()
