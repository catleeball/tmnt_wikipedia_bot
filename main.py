import os
import sys
import time
import wikipedia

from lib import images
from lib import mastodon
from lib import twitter
from lib import words


def main():
    MAX_ATTEMPTS = 1000
    MAX_STATUS_LEN = 280
    BACKOFF = 1
    LOGO_PATH = "/tmp/logo.png"
    CHROME_PATH = "google-chrome-beta"

    title = searchForTMNT(MAX_ATTEMPTS, BACKOFF)
    logo = images.getLogo(title, LOGO_PATH, CHROME_PATH)
    status_text = "\n".join((title, words.getWikiUrl(title)))

    if len(status_text) > MAX_STATUS_LEN:
        status_text = title

    try:
        tweet_status = twitter.sendTweet(status_text, logo)
        toot_status = mastodon.sendToot(status_text, logo)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        sys.exit(1)

    # print(tweet_status)
    # print(toot_status)
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
        if words.isTMNT(title):
            return title
    return False


if __name__ == "__main__":
    main()
