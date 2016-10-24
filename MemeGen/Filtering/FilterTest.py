from BannedWordsFilter import *
from RandomFilter import *

filter = BannedWordsFilter()
filter2 = RandomFilter(1)
tweets = {Tweet('topic', 'body of tweet 1'), Tweet('topic', 'Something offensive towards christians'), Tweet('topic', 'body of tweet 2')}

filteredTweets = filter.filter(tweets)

print ('\n\nFiltered Tweets: ')
for tweet in filteredTweets:
    print(tweet.text)

filteredTweets = filter2.filter(tweets)

print ('\n\nFiltered Tweets: ')
for tweet in filteredTweets:
    print(tweet.text)
