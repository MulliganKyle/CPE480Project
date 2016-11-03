import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'AYP6iDERyueunIWA1Ssvc9MCs'
consumer_secret = 'QwxkVmKSzPtlZqF9iHhcmoZDT0hFp7tOp51DOzXMTtlwpyPOQO'
access_token = '793966158495920128-TqHSdJenOAu9hQgR3vIPFcrbhTlKO7x'
access_secret = 'snfigS1aB72TlG40hHWY0pnCAG7LWD5VGWTc0lumw8nHa'
  
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


api.update_with_media('../MemeGen/successkid.jpg','Updating using OAuth authentication via Tweepy!')
