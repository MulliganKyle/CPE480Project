import os
import re

from Memes.classifiers.helpers import *


POS_MAP = {'DT': [40, 50, 60],
           'IN': [5, 20],
           'NN': [5, 25, 40, 90],
           'NNS': [5, 20, 50, 90],
           'PRP': [5, 18],
           'RB': [5, 18],
           'VBD': [5, 32],
           'JJ': [5, 30, 40, 90]}

OPINION_WORD_LIST = ['should', 'could', 'would', 'dont', 'good', 'better', 'best', 'worse', 'worst', 
  'awesome', 'terrible', 'suck', 'sucks', 'amazing', 'love', 'hate', 'meh', 'probably', 'great']

WORD_LIST = ['do', 'if', 'is', 'or', 'this', 'the', 'she', 'he' ,'I']


# Gets statistics on POS.
def _pos_statistics(pos_tokens):
   pos_map = {pos: 0 for pos in POS_MAP.keys()}

   num_words = 0
   for word, pos in pos_tokens:
      if pos in pos_map:
         pos_map[pos] += 1
         num_words += 1
   pos_map = {pos : int((float(count)/num_words * 100 if num_words else 0))
              for pos, count in pos_map.items()}

   pos_map_ranges = {}
   for key, ranges in POS_MAP.items():
      pos_map_ranges.update(
         create_features_for_ranges(feature_name=key,
                                    variable=pos_map[key],
                                    ranges=ranges))
   return pos_map_ranges


# Determines occurrence of certain words.
def _word_statistics(words, word_list=WORD_LIST):
   fdist = nltk.FreqDist(words)
   features = {}
   for word in word_list:
      features[word] = fdist[word]
   return features


# Determines occurrence of question keywords.
def _word_statistics_opinionated_statements(words):
   features = {}
   features['count_quest_keyword'] = (
      len(OPINION_WORD_LIST) - len(set(OPINION_WORD_LIST) - set(words)))
   features.update(_word_statistics(OPINION_WORD_LIST))
   return features


# Cleans up the tokens.
def _clean_tokens(tokens):
   parsed_tokens = []
   end_reached = False
   for token in tokens:
      if token in [':', '-']:
         parsed_tokens = []
      else:
         token = re.sub(r'[^\w\/\.\,\'\:]+', '', token)
         if token in ['.', '!', '?']:
            end_reached = True
         if token and token.strip() and not end_reached:
            parsed_tokens.append(str(token))
   return parsed_tokens


# Make tokens to lower case.
def _lower_tokens(tokens):
   return [token.lower() for token in tokens]


# Generates the features on the provided statement.
def generate_features(statement):
   tokens = _clean_tokens(get_tokens(statement))
   pos_tokens = nltk.pos_tag(tokens)
   word_tokens = _lower_tokens(tokens)
   features = {}

   features.update(_pos_statistics(pos_tokens))
   #features.update(_word_statistics(word_tokens))
   features.update(_word_statistics_opinionated_statements(word_tokens))
   # TODO(ngarg): Analyze number of stopwords

   return word_tokens, features


def main():
   path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

   # Get data.
   opinionatedStatements = parse_txt_file(filename='opinionatedStatements.txt', path=path, delim="|\n")
   nonOpinionatedStatements = parse_txt_file(filename='wow3k.txt', path=path, delim="|\n")

   #print(opinionatedStatements)
   #return

   # Generate features.
   data = []
   for statement in opinionatedStatements:
      data.append((generate_features(statement)[1], True))
   
   for statement in nonOpinionatedStatements:
      data.append((generate_features(statement)[1], False))

   # Generates training and test set.
   training_data, test_data = split_training_test(data)

   # Generate classifier with score.
   classifier, score = create_classifier(training_data, test_data, debug=True)
   print('classifier score: %.4f' %score)

   # Pickle classifier.
   pickle_classifier(classifier, score, ClassifierType.STATEMENT)


if __name__ == '__main__':
   main()


