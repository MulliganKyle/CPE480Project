# CPE 480: Project (Twitter Meme Bot)

Alex Ehm, Nupur Garg, Kyle Mulligan, Mason Stevenson, Jules Sulpico

   
# Installation

      pip install nltk
      pip install pillow


# Running tests (from project root):

      python -m unittest Twitter.TweetTest
      python -m unittest Filtering.FilterTest
      python -m unittest Memes.MemeClassTest
      python MemeGen/memegenerator.py test-text


# Running program (from project root):

   ### Running Main Programs
   
      python tweet_loader.py
      python generate_meme.py

   ### Generating Classifiers

      python -m Memes.classifiers.generate_questions_classifier 


# Data Sources

   ### Questions (generate_questions_classifier.py)

      http://allysrandomage.blogspot.com/2007/06/101-random-questions.html
      http://www.signupgenius.com/groups/getting-to-know-you-questions.cfm

   ### Sentences

      http://www.jupengineer.com/Reference/300English.pdf
      http://www2.ivcc.edu/rambo/eng1001/sentences.htm
      http://examples.yourdictionary.com/complex-sentence-examples.html
      http://www2.powayusd.com/teachers/kfarrer/Grammar/Holt%20Handbook/Holt%20Chapter%207/Complex%20Sentence.asp
