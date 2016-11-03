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


# Gets the tokens within the statement.
def get_tokens(statement):
   tokenizer = TweetTokenizer()
   tokens = tokenizer.tokenize(statement)
   tokens = [token.lower() for token in tokens]
   return tokens 


# Splits the data made of ({features}: truth) into training and test.
def split_training_test(data, percent=0.75):
   shuffle(data)
   split = int(len(data) * percent)
   training_data = data[:split] 
   test_data = data[split:]
   return (training_data, test_data)


# Creates a Naive Bayes classifier. Returns (classifier, score)
def create_classifier(training_data, test_data):
   classifier = nltk.NaiveBayesClassifier.train(training_data)
   score = nltk.classify.accuracy(classifier, test_data)
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
