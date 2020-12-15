import re
from pathlib import Path

MAX_ATTEMPTS = 450
MAX_STATUS_LEN = 280
BACKOFF = 0.75
TIMEOUT_BACKOFF = 240

HOME = str(Path.home())

# Compiled web screenshot binary: https://github.com/catleeball/WebScreenShot
WSS = "/usr/local/share/tmnt/wss"
# This is a slightly modified version of what's what http://glench.com/tmnt
URL = f"file:///{HOME}/src/tmnt_wikipedia_bot/assets/html/tmnt.html"
SCREENSHOT_PATH = "/tmp/tmnt-logo.png"
KEY_PATH = f"{HOME}/src/tmnt_wikipedia_bot/.keys"
TMNT_STRESSES = re.compile(r"1[02]1[02]1[02]1[02]")
CHARS_ONLY = re.compile("[^a-zA-Z]")

BANNED_WORDS = ("rape", "nazi", "victim", "shootings", "bombing", "bombings")
BANNED_PHRASES = ("shooting", "railway station", "rugby union",
                  "historic district", "murder of", "killing of",
                  "rugby player", ", baron ")  # parens are back, baby  r"("
PRONUNCIATION_OVERRIDES = (("HD", "10"), ("U.S.", "10"), ("Laos", "1"), ("vs.",
                                                                         "10"))
