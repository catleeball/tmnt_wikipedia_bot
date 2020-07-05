import re

# Constants for use throughout the application.
# Someday maybe I'll use configs or CLI args. For now this is easier.

MAX_ATTEMPTS = 1000
MAX_STATUS_LEN = 280
BACKOFF = 0.5
TIMEOUT_BACKOFF = 240

# Compiled web screenshot binary: https://github.com/catleeball/WebScreenShot
WSS = '/usr/local/share/tmnt/wss'
# This is a slightly modified version of what's what http://glench.com/tmnt
URL = 'file:///usr/local/share/tmnt/html/tmnt.html'
SCREENSHOT_PATH = '/tmp/screenshot.png'
KEY_PATH = '/usr/local/share/tmnt/.keys'
TMNT_STRESSES = re.compile(r"1[02]1[02]1[02]1[02]")
CHARS_ONLY = re.compile("[^a-zA-Z]")

# Article titles the contain strings in BANNED_WORDS are skipped.
# Banned words are things that are very inappropriate, or things
# that are oversaturating the timeline, i.e. historic districts
BANNED_WORDS = ("rape", "nazi", "victim", "shootings", "bombing", "bombings")
BANNED_PHRASES = ("shooting", "railway station", "rugby union", "historic district", "murder of", "killing of", "rugby player", ", baron ") # parens are back, baby  r"("
PRONUNCIATION_OVERRIDES = (("HD", "10"), ("U.S.", "10"), ("Laos", "1"), ("vs.", "10"))

