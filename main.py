import os
import pronouncing
import subprocess
import sys
import time
import tweepy
import wikipedia

from collections import namedtuple
from num2words import num2words as n2w
from PIL import Image, ImageChops

# TODO:
#   - Drop titles with words unknown to CMU rather than countin them as 0 stress
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
#   - archive posts locally
#   - cache of titles : stresses

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

    # print(tweet_status)
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
    # Recursion? KISS!
    for ATTEMPT in range(ATTEMPTS):
        print(f"\r{str(ATTEMPT * 10)} articles fetched...", end="")
        sys.stdout.flush()
        title = checkTenPagesForTMNT()

        if type(title) == str and len(title) > 1:
            print(f"\nMatched: {title}")
            return title

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
        time.sleep(120)
        main()
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Wikipedia exception: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception while fetching wiki titles: {e}")
        sys.exit(1)

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
    while title_words:
        if len(title_stresses) > 8:
            return None
        word = title_words.pop(0)
        word_stresses = getWordStresses(word)
        # If word was a long number, it may have been parsed into several words.
        if isinstance(word_stresses, list):
            title_words = word_stresses + title_words
        else:
            title_stresses += getWordStresses(word)

    return title_stresses


def getWordStresses(word: str):
    word = numbersToWords(word)
    if " " in word:
        return word.split()
    try:
        phones = pronouncing.phones_for_word(word)
        stresses = pronouncing.stresses(phones[0])
    except IndexError:
        # Hacky way of discarding candidate title
        return "1111111111"
    return stresses


def numbersToWords(word):
    ordinal_number_endings = ("nd", "rd", "st", "th")
    if word.isdigit():
        if len(word) == 4:
            try:
                word = n2w(word, to="year")
            except Exception:
                # Hacky way of discarding candidate title
                return "1111111111"
        else:
            try:
                word = n2w(word)
            except Exception:
                # Hacky way of discarding candidate title
                return "1111111111"
    if word[:-2].isdigit() and word[-2:] in ordinal_number_endings:
        word = word[-2:]
        try:
            word = n2w(word, to="ordinal")
        except Exception:
            # Hacky way of discarding candidate title
            return "1111111111"

    return word


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
    DEL_CHARS = ["(", ")", "[", "]", "{", "}", ",", ":", ";", "."]
    SWAP_CHARS = [("-", " ")]

    for char in DEL_CHARS:
        s = s.replace(char, "")

    for char, replacement in SWAP_CHARS:
        s = s.replace(char, replacement)

    return s


def getTwitterCredentials(keyfile="/home/cat/src/wiki-turtles/.keys"):
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


def sendTweet(tweet_text: str, image_path=""):
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
        return api.update_with_media(filename=image_path, status=tweet_text)
    else:
        return api.update_status(tweet_text)

    return api.update_status(tweet_text)


def getLogo(title: str):
    title = title.replace(" ", "_")

    chrome_cmd = (
        "google-chrome-beta "
        "--headless "
        "--disable-gpu "
        "--screenshot "
        "--window-size=1280,600 "
        f'"http://glench.com/tmnt/#{title}"'
    )

    retcode = subprocess.run(chrome_cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write("Chrome subprocess exited with code 1")
        sys.exit(1)

    screesnhot_path = "screenshot.png"
    logo_path = cropLogo(screesnhot_path)
    return logo_path


def trimWhitespace(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def cropOffTopAndBottom(image_path: str):
    im = Image.open(image_path)
    w, h = im.size
    return im.crop((0, 175, w, h - 100))


def cropLogo(im):
    logo_path = "/tmp/logo.png"
    im = cropOffTopAndBottom(im)
    im = trimWhitespace(im)
    im.save(logo_path)
    return logo_path


if __name__ == "__main__":
    main()
