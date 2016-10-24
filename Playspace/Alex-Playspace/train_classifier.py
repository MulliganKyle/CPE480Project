import nltk
from nltk.tokenize import word_tokenize
import unicodecsv as csv
import pickle

train = []

csv_file = open("Dataset.csv", "rb")

reader = csv.reader(csv_file)

print "reading file"

read_format_err = 0
row_count = 0
for row in reader:
	if row_count != 0 and row_count <= 500:
		sentiment = int(row[1])
		tweet = row[3]
		if sentiment == 0:
			train.append((tweet, 'negative'))
		elif sentiment == 1:
			train.append((tweet, 'positive'))
		else:
			read_format_err += 1

	row_count += 1

print read_format_err


print "generating all word"
all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))

print "generating use word"
# Use a better technique to filter out meaningless words like 'this', 'that',...
use_words = set([word for word in all_words if len(word) > 2])

print "generating in format for training"
t = [({word: (word in word_tokenize(x[0])) for word in use_words}, x[1]) for x in train]

print "training"

classifier = nltk.NaiveBayesClassifier.train(t)
classifier.show_most_informative_features()

f = open('classifier_100.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

f = open('use_words_100.pickle', 'wb')
pickle.dump(use_words, f)
f.close()


