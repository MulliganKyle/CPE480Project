from random import shuffle


def parse_txt_file():
   return ['hi', 'hello']


def generate_features():
   return {'temp': True}


def split_training_test(data, split=0.75):
   shuffle(data)
   training_data = data[:split] 
   test_data = data[split:]
   return (training_data, test_data)

def main():
   # Get data.
   questions = parse_txt_file('questions.txt')
   statements = parse_txt_file('statements.txt')

   # Generate features.
   data = []
   questions_features = generate_features(questions)
   data.extend([(features, True) for features in questions_features])
   statements_features = generate_features(statements)
   data.extend([(features, False) for features in statements_features])
   
   # Generates training and test set.
   training_data, test_data = split_training_test(data)

   # Generate classifier with score.

   # Pickle classifier.


if __name__ == '__main__':
   main()


