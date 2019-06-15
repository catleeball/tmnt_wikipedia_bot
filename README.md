## TMNT Wikipedia Bot

Every 15 minutes this Python script posts to https://twitter.com/wiki_tmnt

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

### TODO

TODO:
  - More docstrings
  - README
  - CLI arguments
  - use real file format for keys
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
