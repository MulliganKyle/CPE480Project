# 10/21/16
# MemeClass.py
#
# Enum representing the different meme types

import nltk
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

from Memes.classifiers.helpers import unpickle_classifier

wnl=WordNetLemmatizer()

class Meme(object):
   """
   Interface representing a meme.

   filename: str
      Filename of the image.
   """

   def __init__(self, filename, **kwargs):
      self.filename = filename

   # Returns the tokens and tokens tagged with POS
   def _tag_sentence(self, sentence):
      tokens = nltk.tokenize.word_tokenize(sentence)
      return (tokens, nltk.pos_tag(tokens))

   # Gets the verb within the sentence.
   def _find_verbs(self, tagged):
      return [word for word in tagged if 'VB' in word[1]]

   # Gets the plural common nouns within the sentence.
   def _find_common_plural_nouns(self, tagged):
      return [word for word in tagged if word[1] == 'NNS']

   # Transforming the verbs to the present time.
   def _get_basic_form(self, verb):
      return WordNetLemmatizer().lemmatize(verb, wn.VERB)

   # Gets first verb that has a length greater than two.
   def _get_first_verb(self, words):
      for word, pos in words:
         if len(word) > 2 and word[0].isalpha():
            return word
      return None

   # Combines tokens.
   def _combine_tokens(self, tokens):
      string = ''
      prev = ' '
      for token in tokens:
         if token in ['.', '!', '?', ',', ';']:
            string += '.'
         elif token == '@':
            prev = ' @'
         elif token:
            string += '%s%s' %(prev, token)
            prev = ' '
      return string

   def generate(self, tweet):
      # Returns (text, score) tuple.
      raise NotImplementedError()

   def _find_nouns(self, tagged):
      return [word for word in tagged if(word[1] == "NN" or word[1] == "NNP" or word[1] == "NNS" or word[1] == "NNPS")]

   #checks if a word is plural, returns whether it is plural and returns the singular form
   def _isplural(self, word):
      lemma = wnl.lemmatize(word, 'n')
      plural = True if word is not lemma else False
      return plural, lemma

   #gets the singular form of a noun and returns it
   def _get_singular_form(self, noun):
         lemma = wnl.lemmatize(noun, 'n')
         return lemma


class Meme_Doge(Meme):
   """
   Represents a "doge" meme.

   score: int
      Score of the class if matching text is found.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_Doge, self).__init__(filename)
      self.score = kwargs['score']

   def generate(self, tweet):
      return (tweet, self.score)


class Meme_XAllTheY(Meme):
   """
   Represents a "X all the Y" meme.

   score: int
      Score of the class if matching text is found.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_XAllTheY, self).__init__(filename)
      self.score = kwargs['score']

   # Gets first noun that is after the verb.
   def _get_first_noun(self, nouns, tokens, verb_idx):
      for word, pos in nouns:
         if tokens.index(word) > verb_idx:
            return word
      return None

   def generate(self, tweet):
      text = ''
      score = 0.0

      sentence = tweet
      tokens, tagged = self._tag_sentence(sentence)
      verbs = self._find_verbs(tagged)
      nouns = self._find_common_plural_nouns(tagged)

      if verbs and nouns:
         verb = self._get_first_verb(verbs)
         if verb:
            verb_idx = tokens.index(verb)
            verb = self._get_basic_form(verb)
            noun = self._get_first_noun(nouns, tokens, verb_idx)

            if noun:
               text = '%s all the %s!' %(verb, noun)
               score = self.score

      return (text, score)


class Meme_OneDoesNotSimply(Meme):
   """
   Represents a "One Does not Simply" meme.

   score: int
      Score of the class if matching text is found.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_OneDoesNotSimply, self).__init__(filename)
      self.score = kwargs['score']

   def generate(self, tweet):
      text = ''
      score = 0

      sentence = tweet
      tokens, tagged = self._tag_sentence(sentence)
      verbs = self._find_verbs(tagged)

      if verbs:
         verb = self._get_first_verb(verbs)
         if verb:
            verb_idx = tokens.index(verb)
            verb = self._get_basic_form(verb)
            text = 'One does not simply %s%s' %(
                     verb, self._combine_tokens(tokens[verb_idx+1:]))
            score = self.score

      return (text, score)


class Meme_JackieChan(Meme):
   """
   Represents a "Jackie Chan" meme.

   classifier: obj
      ClassifierType indicating the type of classifier.
   func: obj
      Function that gets the features to use for the classifiers.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_JackieChan, self).__init__(filename)
      self.classifier, self.score = unpickle_classifier(kwargs['classifier'])
      self.func = kwargs['func']

   def generate(self, tweet):
      tokens, features = self.func(tweet)
      result = self.classifier.classify(features)

      if result:
         text = ' '.join(tokens) + '?'
         return (text, self.score)
      return ('', 0)

class Meme_JackieChan_Hashtag(Meme):
   """
   Represents a "Jackie Chan" meme.

   classifier: obj
      ClassifierType indicating the type of classifier.
   func: obj
      Function that gets the features to use for the classifiers.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_JackieChan_Hashtag, self).__init__(filename)
      self.classifier, self.score = unpickle_classifier(kwargs['classifier'])
      self.func = kwargs['func']

   def generate(self, tweet):
      features = self.func(tweet)
      result = self.classifier.classify(features)

      if result:
         return (tweet, self.score)
      return ('', 0)


class Meme_Kermit(Meme):
   """
   Represents a "Kermit" meme.

   classifier: obj
      ClassifierType indicating the type of classifier.
   func: obj
      Function that gets the features to use for the classifiers.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_Kermit, self).__init__(filename)
      self.classifier, self.score = unpickle_classifier(kwargs['classifier'])
      self.func = kwargs['func']

   def generate(self, tweet):
      tokens, features = self.func(tweet)
      result = self.classifier.classify(features)

      if result:
         text = tweet + ' but thats none of my business'
         return (text, self.score)
      return ('', 0)

class Meme_Profession(Meme):
   """
   Represents a "Profession" meme.

   classifier: obj
      ClassifierType indicating the type of classifier.
   func: obj
      Function that gets the features to use for the classifiers.
   """

   def __init__(self, filename, **kwargs):
      super(Meme_Profession, self).__init__(filename)
      self.score = kwargs['score']

   def generate(self, tweet):
      text = ''
      score = 0.0

      tokens, tagged = self._tag_sentence(tweet)
      nouns = self._find_nouns(tagged)
      singularNouns = []
      if(len(nouns)>0):
         score = self.score
         for noun in nouns:
            singularNouns.append(self._get_singular_form(noun[0]))

         for noun in singularNouns:
            if (noun[0] == 'a' or noun[0] == 'e' or noun[0] == 'i' or noun[0] == 'o' or noun[0] == 'u' or noun[0] == 'A' or noun[0] == 'E' or noun[0] == 'I' or noun[0] == 'O' or noun[0] == 'U'):
               text = "I used to be an " + noun + " like you, but then I took an arrow to the knee."
            else:
               text = "I used to be a " + noun + " like you, but then I took an arrow to the knee."

      return text, score
