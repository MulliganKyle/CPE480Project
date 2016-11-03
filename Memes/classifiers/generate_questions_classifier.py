import os

from Memes.classifiers.helpers import *



# Generates the features on the provided statement.
def generate_features(statement):
   tokens = get_tokens(statement)
   features = {}

   # Generates features based on questions keywords.
   question_keywords = ['what', 'when', 'where', 'why', 'who', 'how']
   for keyword in question_keywords:
      features['contains_%s' %keyword] = keyword in tokens

   return features



def main():
   path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

   # Get data.
   questions = parse_txt_file(filename='questions.txt', path=path)
   statements = parse_txt_file(filename='statements.txt', path=path)

   # Generate features.
   data = []
   for question in questions:
      data.append((generate_features(question), True))
   for statement in statements:
      data.append((generate_features(statement), False))

   # Generates training and test set.
   training_data, test_data = split_training_test(data)

   # Generate classifier with score.
   classifier, score = create_classifier(training_data, test_data)
   print 'classifier score: %.4f' %score

   # Pickle classifier.
   pickle_classifier(classifier, score, ClassifierType.QUESTION)


if __name__ == '__main__':
   main()


