import sys

from mastodon import Mastodon

def getMastodonCredentials(keyfile="/home/cat/src/wiki-turtles/.keys"):
    # TODO: Use better config file format, better parsing logic
    # TODO: This largely repeats the twitter.py credential logic. Make
    #       this generic for both to use to use, and only open the keyfile
    #       once.
    try:
        with open(keyfile, "r") as f:
            keys = f.read()
    except Exception as e:
        sys.stderr.write(f"Exception fetching Twitter keys: {e}")
        sys.exit(1)

    keys = keys.split()
    keys = [key.strip() for key in keys]

    try:
        api = Mastodon(
            access_token=keys[4],
            api_base_url=keys[5] or "https://botsin.space",
        )
    except IndexError as e:
        sys.stderr.write(f"Lines 4 and 5 of {keyfile} not found. {e}")
        return False
    except Exception as e:
        sys.stderr.write(f"Exception creating mastodon client. {e}")
    
    try:
        api.log_in(
            username=keys[6],
            password=keys[7],
        )
    except IndexError as e:
        sys.stderr.write(f"Lines 6 and 7 of {keyfile} not found. {e}")
        return False
    except Exception as e:
        sys.stderr.write(f"Exception authing mastodon client. {e}")
        return False
    
    return api


def sendToot(toot_text: str, image_path=""):
    api = getMastodonCredentials(keyfile="/home/cat/src/wiki-turtles/.keys")
    if api:
        media_id = api.media_post(image_path)["id"]
        return api.status_post(
            status=toot_text,
            media_ids=[media_id],
        )
