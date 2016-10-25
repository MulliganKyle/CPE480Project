# 10/21/16
# MemeClass.py
#
# Enum representing the different meme types

import nltk
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn


# TODO: REMOVE!
class MemeType(object):
   """
   Enum representing the type of Meme object.
   """
   UNKNOWN = 1
   DOGE = 2
   XY = 3
   BOROMIR = 4
   JACKIE_CHAN = 5
   KERMIT = 6
   GAASTON = 7
   SKYRIM = 8
   WONKA = 9


class Meme(object):
   """
   Interface representing a meme.

   score: int 
      Score of the class if matching text is found.
   """

   def __init__(self, score):
      self.score = score

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
      # TODO: RETURN SOME TWEET OBJECT
      raise NotImplementedError()


class Meme_Doge(Meme):
   """
   Represents a "doge" meme.
   """

   def generate(self, tweet):
      # TODO: FINISH
      return (tweet.text, self.score)



class Meme_XAllTheY(Meme):
   """
   Represents a "doge" meme.
   """

   # Gets first noun that is after the verb.
   def _get_first_noun(self, nouns, tokens, verb_idx):
      for word, pos in nouns:
         if tokens.index(word) > verb_idx:
            return word
      return None

   def generate(self, tweet):
      text = ''
      score = 0.0

      sentence = tweet.text
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
   Represents a "doge" meme.
   """

   def generate(self, tweet):
      text = ''
      score = 0

      sentence = tweet.text
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



