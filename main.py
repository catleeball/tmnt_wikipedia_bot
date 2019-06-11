import pronouncing
import sys
import time
import tweepy
import wikipedia

from collections import namedtuple

# TODO:
#   - Docstrings
#   - README
#   - CLI arguments
#   - Image generator
#   - Twitter linkup
#   - Tests
# Super bonus points:
#   - CI
#   - Mastodon

TwitterAuth = namedtuple(
    "TWITTER",
    ["consumer_key", "consumer_secret", "access_token", "access_token_secret"],
)

TWITTER = TwitterAuth(
    consumer_key="xxx",
    consumer_secret="yyy",
    access_token="aaa",
    access_token_secret="bbb",
)


def main():
    ATTEMPTS = 100
    BACKOFF = 2

    for i in range(ATTEMPTS):
        print(f"\rAttempt: {str(i)} / {str(ATTEMPTS)}", end="")
        checkPages()
        time.sleep(BACKOFF)

    print(f"No matches found in {str(ATTEMPTS * 10)} pages.")
    sys.exit(1)


def checkPages():
    titles = wikipedia.random(10)
    for title in titles:
        if isTMNT(title):
            sys.stdout.flush()
            print(f"\nMatch: {title}")
            sys.exit(0)


def isTMNT(title: str):
    """Checks if a Wikipedia page title has the same stress pattern as TMNT.

    >>> isTMNT('Teenage Mutant Ninja Turtles')
    True

    >>> isTMNT('Single Payer Health Insurance')
    True

    >>> isTMNT('Romeo, Romeo, wherefore art thou, Romeo?')
    False
    """
    TMNT_STRESSES = ("12101010", "11101010", "10101010")

    title = cleanStr(title)
    title_stresses = getTitleStresses(title)

    if not title_stresses:
        return False

    if len(title_stresses) != 8:
        return False

    return title_stresses in TMNT_STRESSES


def getTitleStresses(title: str):
    """Takes a wikipedia title and gets the combined stresses of all words.

    >>> getTitleStresses('Teenage Mutant Ninja Turtles')
    '12101010'

    Args:
        title: String, title of a wikipedia page.
    Returns:
        String, stresses of each syllable as 0, 1, and 2s.
    """
    title_words = title.split()
    title_stresses = ""
    for word in title_words:
        title_stresses += getWordStresses(word)
        if len(title_stresses) > 8:
            return None
    return title_stresses


def getWordStresses(word: str):
    try:
        phones = pronouncing.phones_for_word(word)
        stresses = pronouncing.stresses(phones[0])
    except IndexError:
        return ""
    return stresses


def cleanStr(s: str):
    """Remove characters that the pronouncing dictionary doesn't like.

    This isn't very efficient, but it's readable at least. :-)

    >>> cleanStr('fooBar123')
    'fooBar123'

    >>> cleanStr('Hello ([world])')
    'Hello world'

    >>> cleanStr('{hello-world}')
    'hello world'

    Args:
        s: String to be stripped of offending characters
    Returns:
        String without offending characters
    """
    DEL_CHARS = ["(", ")", "[", "]", "{", "}", ","]
    SWAP_CHARS = [("-", " ")]

    for char in DEL_CHARS:
        if char in s:
            s = s.replace(char, "")

    for char, replacement in SWAP_CHARS:
        if char in s:
            s.replace(char, replacement)

    return s


def sendTweet(tweet_text: str, image_path=""):
    """Post some text, and optionally an image to twitter.

    Params:
        tweet_text: String, text to post to twitter, must be less than 260 chars
        image_path: String, path to image on disk to be posted to twitter
    Returns:
        tweepy.status object, contains response from twitter request
    """
    auth = tweepy.OAuthHandler(TWITTER.consumer_key, TWITTER.consumer_secret)
    auth.set_access_token(TWITTER.access_token, TWITTER.access_token_secret)

    api = tweepy.API(auth)

    if image_path:
        return api.update_with_media(tweet_text, image_path)

    return api.update_status(tweet_text)


if __name__ == "__main__":
    main()
