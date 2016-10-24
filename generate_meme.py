import nltk
#import pickle
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

from Filtering.BannedWordsFilter import BannedWordsFilter
from Filtering.RandomFilter import RandomFilter
from Twitter.Tweet import Tweet

# Broken, import not working.

# Tags the sentence with POS.
def tag_sentence(sentence):
   tokenized = nltk.tokenize.word_tokenize(sentence)
   return nltk.pos_tag(tokenized)

# Gets the verb within the sentence.
def find_verbs(tagged):
   return [word for word in tagged if word[1].find('VB') >= 0]

# Gets the plural nouns within the sentence.
def find_plural_nouns(tagged):
   return [word for word in tagged if(word[1] == "NNS" or word[1] == "NNPS")]

# Transforming the verbs to the present time.
def get_basic_form(verb):
   return WordNetLemmatizer().lemmatize(verb, wn.VERB)

# Filtering out forms of 'be' becuase it's not useful in the memes.
def get_first_not_be(verbs):
   for verb, pos in verbs:
      if get_basic_form(verb) != 'be':
         return verb
   return None

# Generates a string for "One does not simply" meme.
def one_does_not_simply(sentence):
   tagged = tag_sentence(sentence)
   verbs = find_verbs(tagged)
   if len(verbs) > 0:
      verb = next((verb[0] for verb in verbs if get_basic_form(verb[0])!='be'), None)
      if verb is not None:
         pos = sentence.find(verb)
         basicVerb = get_basic_form(verb)
         return "One does not simply " + basicVerb + sentence[pos + len(verb):]

# Generates the "x all the y" meme.
def x_all_the_y(sentence):
   tagged = tag_sentence(sentence)
   verbs = find_verbs(tagged)
   nouns = find_plural_nouns(tagged)
   verb = get_first_not_be(verbs)
   
   if verb is not None and len(nouns) > 0:
      verbPos = sentence.find(verb)
      verb = get_basic_form(verb)
      noun = next((noun[0] for noun in nouns if sentence.find(noun[0]) > verbPos), None)
      if noun is not None:
         return verb + " all the " + noun + "!"

def generator():
   # Get tweets.
   dump = open("Twitter/Dumps/SerializedTweets.p", "rb")
#   tweets = pickle.load(dump)
   tweets = set([Tweet('topic', 'this is the tweet')])

   # Get single tweet.
   banned_filter = BannedWordsFilter()
   filtered_tweets = banned_filter.filter(tweets)
   random_filter = RandomFilter(1)
   tweet = random_filter.filter(filtered_tweets)[0]

   # Takes action based on tweet.
   if one_does_not_simply(tweet.text) is not None:
      print one_does_not_simply(tweet.text)
   elif x_all_the_y(tweet.text) is not None:
      print x_all_the_y(tweet.text)
   else:
      # Doge as default
      print tweet.text
   

if __name__ == "__main__":
   generator()
