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
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from Twitter.Tweet import *
from Memes.classifiers.helpers import *

PATH = "Twitter/Dumps/"

def generate_features():
   return


def clean_tweets(tweets):
   # Remove hashtags, @'s, emojis

   for tweet in tweets:
      #print tweet.text
      tweet.text = ' '.join(word for word in tweet.text.split(' ')
                                 if not word.startswith('#') and not word.startswith('@'))
      tweet.text = re.sub('[^\w\/\$\!\.\,\?\ \-\']+', ' ', tweet.text)
      #print tweet.text

#extrat single words as features from the training data
def generate_unigram_feature_list(training_data):
   unigram_features = set(word.lower() for passage in training_data for word in word_tokenize(passage))
   unigram_features = set(word for word in unigram_features if word not in stopwords.words("english"))
   unigram_features = set(word for word in unigram_features if word not in string.punctuation)
   return unigram_features

#extract bigrams as features form the training data
def generate_bigram_feature_list(training_data):
   features_bigrams = set()
   for sentence in training_data:
      for gram in ngrams(word_tokenize(sentence), 2):
         if gram not in features_bigrams:
            features_bigrams.add(gram)
   features_bigrams = set(bigram for bigram in features_bigrams 
                                 if bigram[0] not in stopwords.words("english") 
                                 and bigram[1] not in stopwords.words("english"))
   features_bigrams = set(bigram for bigram in features_bigrams 
                                 if bigram[0] not in string.punctuation 
                                 and bigram[1] not in string.punctuation)
   return features_bigrams


def generate_features(tweet, word_features = None, features_bigrams = None):
   if word_features is None:
      f = open('Memes/classifiers/hashtag_word_features.p', 'rb')
      word_features = pickle.load(f)
      f.close()
   if features_bigrams is None:
      f = open('Memes/classifiers/hashtag_bigram_features.p', 'rb')
      features_bigrams = pickle.load(f)
      f.close()

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

   # Unpickle tweets
   dump_waitwhat = open(PATH + "waitwhat_dump.p" , "rb")
   dump_justdoit = open(PATH + "justdoit_dump.p" , "rb")
   dump_unambiguous = open(PATH + "unambiguous_dump.p" , "rb")

   tweets_waitwhat = pickle.load(dump_waitwhat)
   tweets_justdoit = pickle.load(dump_justdoit)
   tweets_unambiguous = pickle.load(dump_unambiguous)

   # Scrub tweets
   clean_tweets(tweets_waitwhat)
   clean_tweets(tweets_justdoit)
   clean_tweets(tweets_unambiguous)


   confused_tweets = set(tweet.text for tweet in tweets_waitwhat)
   not_confused_tweets = set(tweet.text for tweet in tweets_justdoit) | set(tweet.text for tweet in tweets_unambiguous)


   confused_tweets = [x.lower() for x in confused_tweets]
   not_confused_tweets = [x.lower() for x in not_confused_tweets]
   all_tweets = confused_tweets + not_confused_tweets   

   # Extract the features from the training data
   word_features = generate_unigram_feature_list(all_tweets)
   bigram_features = generate_bigram_feature_list(all_tweets)

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

   #Pickle the extracted features
   f = open('Memes/classifiers/hashtag_word_features.p', 'wb')
   pickle.dump(word_features, f)
   f.close()
   f = open('Memes/classifiers/hashtag_bigram_features.p', 'wb')
   pickle.dump(bigram_features, f)
   f.close()







# Throw tweet through classifiers


if __name__ == '__main__':
    main()
