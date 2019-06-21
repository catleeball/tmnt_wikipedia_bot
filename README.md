## TMNT Wikipedia Bot

Every 60 minutes this Python script posts to https://twitter.com/wiki_tmnt and https://botsin.space/@tmnt

### Why

For fun! Inspired by https://xkcd.com/1412/

### How

When it runs, it:
- Pulls 10 random Wikipedia article titles
- Checks if they are in trochaic tetrameter
  - If not, pull 10 more articles ad hominum until a match is found
- Create a faux-TMNT logo containing the wiki title
  - I'm using the logic at http://glench.com/tmnt to do this
- Post the title and generated logo to @wiki_tmnt on Twitter

### Environment

This script requires the following:

- Python >= 3.7
  - Earlier may work, only tested on 3.7
- Chrome >= 57
- Via PyPi:
  - pronouncing
  - num2words
  - PIL

For @wiki_tmnt it runs on a cron job on my local machine.

### Configuration

I haven't defined a config file format yet, it's in the TODO list below. Common config knobs are currently mostly in `lib/constants.py`.

### Caveats

I'm not developing this for anyone but myself, so you may see some anti-patterns like hardcoded paths specific to my environment, and general lack of configurability outside editing the source.

### TODO

TODO:
  - More docstrings
  - README
  - CLI arguments
  - use real file format for keys
  - refactor key fetching to be done once
  - Integration tests
  - more unit tests
  - actually enable option to run doctests
  - Run glench.com/tmnt locally

Super bonus points:
  - CI
  - Mastodon
  - zipapp release
  - archive posts locally
  - cache of titles : stresses
