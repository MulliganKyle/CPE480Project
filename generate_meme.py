import nltk
import pickle

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from Filtering.BannedWordsFilter import BannedWordsFilter
#from Filtering.RandomFilter import RandomFilter
#from Twitter.Tweet import Tweet

# Broken, import not working.

def generator():
   print 'Inside generate_meme.py'
   dump = open("Twitter/Dumps/SerializedTweets.p", "rb")
   tweets = pickle.load(dump)
   banned_filter = BannedWordsFilter()
   filtered_tweets = tweet_filter.filter(tweets)
   random_filter = RandomFilter(1)
   meme_tweet = tweet_filter.filter(filtered_tweets)[0]
   if(one_does_not_simply(tweet.text) is not None):
      print one_does_not_simply(tweet.text)
   elif(x_all_the_y(tweet.text) is not None):
      print x_all_the_y(tweet.text)
   else:
      #Doge as default
      print tweet.text
   

if __name__ == "__main__":
   generator()

def tag_sentence(sentence):
   tokenized = nltk.tokenize.word_tokenize(sentence)
   return nltk.pos_tag(tokenized)

def find_verbs(tagged):
	return [word for word in tagged if word[1].find('VB') >= 0]

def find_plural_nouns(tagged):
	return [word for word in tagged if(word[1] == "NNS" or word[1] == "NNPS")]

def get_basic_form(verb):
	return WordNetLemmatizer().lemmatize(verb,wn.VERB)

def get_first_not_be(verbs):
	return next((verb[0] for verb in verbs if get_basic_form(verb[0])!='be'), None)

def one_does_not_simply(sentence):
	tagged = tag_sentence(sentence)
	verbs = find_verbs(tagged)
	if(len(verbs) > 0):
		verb = next((verb[0] for verb in verbs if get_basic_form(verb[0])!='be'), None)
		if verb is not None:
			pos = sentence.find(verb)
			basicVerb = get_basic_form(verb)
			return "One does not simply " + basicVerb + sentence[pos + len(verb):]

def x_all_the_y(sentence):
	tagged = tag_sentence(sentence)
	verbs = find_verbs(tagged)
	nouns = find_plural_nouns(tagged)
	verb = get_first_not_be(verbs)
	verbPos = sentence.find(verb)
	verb = get_basic_form(verb)
	if(verb is not None and len(nouns) > 0):
		noun = next((noun[0] for noun in nouns if sentence.find(noun[0]) > verbPos), None)
		if noun is not None:
			return verb + " all the " + noun + "!"
