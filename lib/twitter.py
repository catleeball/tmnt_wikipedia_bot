import sys
import tweepy
from lib import keys as k

def sendTweet(tweet_text: str, image_path=""):
    """Post some text, and optionally an image to twitter.

    Args:
        tweet_text: String, text to post to twitter, must be less than 260 chars
        image_path: String, path to image on disk to be posted to twitter
    Returns:
        tweepy.status object, contains response from twitter request
    """
    auth = tweepy.OAuthHandler(k.TWITTER_CONSUMER_KEY, k.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(k.TWITTER_ACCESS_TOKEN, k.TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    if image_path:
        return api.update_with_media(filename=image_path, status=tweet_text)
    else:
        return api.update_status(tweet_text)

    return api.update_status(tweet_text)
