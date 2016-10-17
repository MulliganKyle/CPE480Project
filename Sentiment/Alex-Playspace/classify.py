import nltk
from nltk.tokenize import word_tokenize
import pickle

# Load classifier and Word List
# TODO: Find a way to not dump and load the wordlist.

f = open('classifier_100.pickle', 'rb')
classifier = pickle.load(f)
f.close()

f = open('use_words_100.pickle', 'rb')
use_words = pickle.load(f)
f.close()


while True:
	to_classify = raw_input("Type a sentence to classify ")
	test_sent_features = {word.lower(): (word in word_tokenize(to_classify.lower())) for word in use_words}
	classified = classifier.classify(test_sent_features)

	print classified
