import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

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



print one_does_not_simply("I sit at home bored")
print one_does_not_simply("He is is be just want to get his work done")
print one_does_not_simply("I am jumping around")
print one_does_not_simply("I am really bored")
print one_does_not_simply("Banana Apple Tomato.")

print x_all_the_y("I eat an apple")
print x_all_the_y("I am eating  a lot of apples")
print x_all_the_y("We are sitting on couches")

 


 



