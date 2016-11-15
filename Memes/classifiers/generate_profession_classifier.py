import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn


wnl=WordNetLemmatizer()

def tag_sentence(sentence):
   tokenized = nltk.tokenize.word_tokenize(sentence)
   return nltk.pos_tag(tokenized)

#finds all nouns in a tagged sentence and returns a list of them
def find_nouns(tagged):
   return [word for word in tagged if(word[1] == "NN" or word[1] == "NNP" or word[1] == "NNS" or word[1] == "NNPS")]

#checks if a word is plural, returns whether it is plural and returns the singular form
def isplural(word):
   lemma = wnl.lemmatize(word, 'n')
   plural = True if word is not lemma else False
   return plural, lemma

#gets the singular form of a noun and returns it
def get_singular_form(noun):
      isp, lemma = isplural(noun)
      return lemma

#generates arrow to the knee meme text for input sentence
def arrow_to_the_knee(sentence):
   tagged = tag_sentence(sentence)
   nouns = find_nouns(tagged)
   singularNouns = []
   if(len(nouns)>0):
      for noun in nouns:
	 singularNouns.append(get_singular_form(noun[0]))

      for noun in singularNouns:
	 if (noun[0] == 'a' or noun[0] == 'e' or noun[0] == 'i' or noun[0] == 'o' or noun[0] == 'u' or noun[0] == 'A' or noun[0] == 'E' or noun[0] == 'I' or noun[0] == 'O' or noun[0] == 'U'):
	    print "I used to be an " + noun + " like you, but then I took an arrow to the knee."
	 else:
	    print "I used to be a " + noun + " like you, but then I took an arrow to the knee."

arrow_to_the_knee("Apple orange bananas")
arrow_to_the_knee("Sometimes I eat steak or hamburgers.")
arrow_to_the_knee("This Is the only thing being accomplished by all the crybabies blocking the streets!")
