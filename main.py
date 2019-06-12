import pronouncing
import sys
import time
import tweepy
import wikipedia

from collections import namedtuple
from PIL import Image, ImageChops
from selenium import webdriver

# TODO:
#   - Docstrings
#   - README
#   - CLI arguments
#   - Image generator
#   - Get twitter credentials from somewhere not inline with the code
#   - More tests
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
    MAX_ATTEMPTS = 1000
    BACKOFF = 1

    title = searchForTMNT(MAX_ATTEMPTS, BACKOFF)

    if title:
        print(f"\nMatch: {title}")
        sys.exit(0)

    print(f"\nNo matches found in {str(MAX_ATTEMPTS * 10)} pages.")
    sys.exit(1)


def searchForTMNT(ATTEMPTS=100, BACKOFF=1):
    """Loop MAX_ATTEMPT times, searching for a TMNT meter wikipedia title.

    Args:
        Integer: ATTEMPTS, retries remaining.
        Integer: BACKOFF, seconds to wait between each loop.
    Returns:
        String or False: String of wikipedia title in TMNT meter, or False if
                         none found.
    """
    if ATTEMPTS <= 0:
        sys.stdout.flush()
        return False

    sys.stdout.flush()
    print(f"\rAttempts remaining: {str(ATTEMPTS)}", end="")
    maybeValidTitle = checkTenPagesForTMNT()

    if maybeValidTitle:
        sys.stdout.flush()
        return maybeValidTitle
    else:
        time.sleep(BACKOFF)
        searchForTMNT(ATTEMPTS - 1, BACKOFF)


def checkTenPagesForTMNT():
    """Get 10 random wiki titles, check if any of them isTMNT().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in TMNT meter, return the title. Otherwise, return False.

    Args:
        None
    Returns:
        String or False: The TMNT compliant title, or False if none found.
    """
    titles = wikipedia.random(10)
    for title in titles:
        if isTMNT(title):
            return title
    return False


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
            s = s.replace(char, replacement)

    return s


def sendTweet(tweet_text: str, image_path=""):
    """Post some text, and optionally an image to twitter.

    Args:
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


def getLogo(title):
    title = title.replace(" ", "_")
    scripts = (
        "document.getElementsByTagName('P')[0].style.visibility = 'hidden'",
        "document.getElementById('logo-text').style.visibility = 'hidden'",
        # "driver.execute_script("document.getElementById('share').style.visibility = 'hidden'",
    )

    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.set_window_size(800, 600)
    driver.get(f"http://glench.com/tmnt/#{title}")

    for script in scripts:
        driver.execute_script(script)

    driver.save_screenshot(f"logos/{title}.png")
    driver.quit()


def trimWhitespace(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def cropBottom20px(im):
    w, h = im.size
    return im.crop((0, 0, w, h - 20))


def cropLogo(image_path):
    im = Image.open(image_path)
    im = trimWhitespace(im)
    im = cropBottom20px(im)
    im = trimWhitespace(im)
    im.save(image_path)


if __name__ == "__main__":
    main()
