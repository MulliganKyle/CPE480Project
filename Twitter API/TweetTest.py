# Test Tweet class constructor
from Tweet import *

tweet1 = Tweet('topic1', 'text1')
tweet2 = Tweet('topic2', 'text2')
tweet3 = Tweet('topic3', 'text3')

print ('tweet1 memeClass: ')
print (tweet1.memeClass)

tweet1.memeClass = MemeClass.KERMIT

print ('tweet1 memeClass: ')
print (tweet1.memeClass)
