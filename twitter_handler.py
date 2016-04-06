import tweepy
from twitter_config import config

class TwitterHandler(object):
    def __init__(self):
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
        auth.set_access_token(config["access_key"], config["access_secret"])
        self.api = tweepy.API(auth)
    
    def send_tweet(self, tweet_message):
        self.api.update_status(tweet_message)
