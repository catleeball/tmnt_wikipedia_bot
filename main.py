import os
import pronouncing
import sys
import time
import tweepy
import wikipedia

from collections import namedtuple
from PIL import Image, ImageChops
from selenium import webdriver

# TODO:
#   - More docstrings
#   - README
#   - CLI arguments
#   - use real file format for keys
#   - Integration tests
#   - more unit tests
#   - actually enable option to run doctests
# Super bonus points:
#   - CI
#   - Mastodon

TwitterAuth = namedtuple(
    "TWITTER",
    ["consumer_key", "consumer_secret", "access_token", "access_token_secret"],
)


def main():
    MAX_ATTEMPTS = 1000
    BACKOFF = 1

    title = searchForTMNT(MAX_ATTEMPTS, BACKOFF)
    logo = getLogo(title)

    try:
        tweet_status = sendTweet(title, logo)
    except OSError as e:
        sys.stderr.write(f"Unable to read logo file {logo}. Error: {e}")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        sys.exit(1)

    #print(tweet_status)
    sys.exit(0)


def searchForTMNT(ATTEMPTS=1000, BACKOFF=1):
    """Loop MAX_ATTEMPT times, searching for a TMNT meter wikipedia title.

    Args:
        Integer: ATTEMPTS, retries remaining.
        Integer: BACKOFF, seconds to wait between each loop.
    Returns:
        String or False: String of wikipedia title in TMNT meter, or False if
                         none found.
    """
    return "Edward Collins (figure skater)"
    # Recursion? KISS!
    for ATTEMPT in range(ATTEMPTS):
        print(f"\r{str(ATTEMPT)} attempts remaining...", end="")
        sys.stdout.flush()
        maybeValidTitle = checkTenPagesForTMNT()

        if type(maybeValidTitle) == str and len(maybeValidTitle) > 1:
            print(f"\nMatched: {maybeValidTitle}")
            return maybeValidTitle

        time.sleep(BACKOFF)

    print(f"\nNo matches found.")
    sys.exit(1)


def checkTenPagesForTMNT():
    """Get 10 random wiki titles, check if any of them isTMNT().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in TMNT meter, return the title. Otherwise, return False.

    Args:
        None
    Returns:
        String or False: The TMNT compliant title, or False if none found.
    """
    wikipedia.set_rate_limiting(True)
    try:
        titles = wikipedia.random(10)
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"Wikipedia timout exception: {e}")
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Wikipedia exception: {e}")
    except Exception as e:
        print(f"Exception while fetching wiki titles: {e}")

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
    DEL_CHARS = ["(", ")", "[", "]", "{", "}", ",", ":", ";"]
    SWAP_CHARS = [("-", " ")]

    for char in DEL_CHARS:
        if char in s:
            s = s.replace(char, "")

    for char, replacement in SWAP_CHARS:
        if char in s:
            s = s.replace(char, replacement)

    return s


def getTwitterCredentials(keyfile=".keys"):
    # TOODO: Use better config file format, better parsing logic
    try:
        with open(keyfile, "r") as f:
            keys = f.read()
    except Exception as e:
        sys.stderr.write(f"Exception fetching Twitter keys: {e}")
        sys.exit(1)

    keys = keys.split()
    keys = [key.strip() for key in keys]

    return TwitterAuth(
        consumer_key=keys[0],
        consumer_secret=keys[1],
        access_token=keys[2],
        access_token_secret=keys[3],
    )


def sendTweet(tweet_text: str, image_path="/tmp/logo.png"):
    """Post some text, and optionally an image to twitter.

    Args:
        tweet_text: String, text to post to twitter, must be less than 260 chars
        image_path: String, path to image on disk to be posted to twitter
    Returns:
        tweepy.status object, contains response from twitter request
    """
    TWITTER = getTwitterCredentials()
    auth = tweepy.OAuthHandler(TWITTER.consumer_key, TWITTER.consumer_secret)
    auth.set_access_token(TWITTER.access_token, TWITTER.access_token_secret)

    api = tweepy.API(auth)

    if image_path:
        return api.update_with_media(
            filename=image_path, status=tweet_text)
    else:
        return api.update_status(tweet_text)

    return api.update_status(tweet_text)


def getLogo(title: str):
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

    logo_path = "logo.png"
    driver.save_screenshot(logo_path)
    time.sleep(1)
    cropLogo(logo_path)
    time.sleep(1)
    driver.quit()
    time.sleep(3)
    return logo_path


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


def cropLogo(image_path: str):
    im = Image.open(image_path)
    im = trimWhitespace(im)
    im = cropBottom20px(im)
    im = trimWhitespace(im)
    im.save(image_path)


if __name__ == "__main__":
    main()
