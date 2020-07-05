import sys
from lib import keys as k
from mastodon import Mastodon

def sendToot(toot_text: str, image_path=""):
    api = Mastodon(access_token=k.MASTO_ACCESS_TOKEN, api_base_url=k.MASTO_URL)
    api.log_in(username=k.MASTO_UNAME, password=k.MASTO_PW)
    if api:
        media_id = api.media_post(image_path)["id"]
        return api.status_post(status=toot_text, media_ids=[media_id])
