from nltk.tokenize import TweetTokenizer
from random import shuffle
import pickle
import nltk
import os


# Enum of classifier type.
class ClassifierType:
   HASHTAG = 1
   QUESTION = 2
   PROFESSION = 3
   STATEMENT = 4


# Parses a text file into a list.
def parse_txt_file(filename, path):
   full_filename = os.path.join(path, filename)
   with open(full_filename) as f:
      lines = [line.strip() for line in f.readlines()]
      return lines
   raise Error('File not found')

# Parses a text file into a list. Uses delim to break apart the file
def parse_txt_file(filename, path, delim):
   full_filename = os.path.join(path, filename)
   with open(full_filename) as f:
      lines = [line.strip() for line in f.read().split(delim)]
      return lines
   raise Error('File not found')


# Gets the tokens within the statement.
def get_tokens(statement):
   tokenizer = TweetTokenizer()
   tokens = tokenizer.tokenize(statement)
   return tokens 


# Generates features based on ranges.
def create_features_for_ranges(feature_name, variable, ranges):
   features = {'%s_<_%d' %(feature_name, ranges[0]): variable < ranges[0]}
   if len(ranges) > 1:
      features['%s_>=_%d' %(feature_name, ranges[-1])] = variable >= ranges[-1]
      for min_range, max_range in zip(ranges, ranges[1:]):
         feature = '%s_%d_to_%d' %(feature_name, min_range, max_range)
         features[feature] = variable >= min_range and variable < max_range
   return features


# Splits the data made of ({features}: truth) into training and test.
def split_training_test(data, percent=0.75):
   shuffle(data)
   split = int(len(data) * percent)
   training_data = data[:split] 
   test_data = data[split:]
   return (training_data, test_data)


# Creates a Naive Bayes classifier. Returns (classifier, score)
def create_classifier(training_data, test_data, debug=False):
   classifier = nltk.NaiveBayesClassifier.train(training_data)
   score = nltk.classify.accuracy(classifier, test_data)

   if debug:
      print('__Result__\t\t__Actual__')
      for features, actual in test_data:
         result = classifier.classify(features)
         print('%s\t\t\t%s' %(result, actual))
      classifier.show_most_informative_features(30)
      print('Score: %.4f' %score)

   return classifier, score


# Gets the pickle filename.
def _get_pickle_filename(pickle_type):
   path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
   filename = 'classifier_%d.pickle' %pickle_type
   full_filepath = os.path.join(path, filename)
   return full_filepath


# Pickes the (classifier, score) into the filename provided.
def pickle_classifier(classifier, score, pickle_type):
   filename = _get_pickle_filename(pickle_type)
   pickle.dump((classifier, score), open(filename, 'wb'))


# Unpickles the classifier. Returns (classifier, score).
def unpickle_classifier(pickle_type):
   filename = _get_pickle_filename(pickle_type)
   classifier, score = pickle.load(open(filename, 'rb'))
   return classifier, score
