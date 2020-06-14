## TMNT Wikipedia Bot

Every 60 minutes this Python script posts to https://twitter.com/wiki_tmnt and https://botsin.space/@tmnt

### Why

For fun! Inspired by https://xkcd.com/1412/

### How

When it runs, it:
- Pulls 10 random Wikipedia article titles
- Checks if titles are in trochaic tetrameter
  - If not, pull 10 more articles ad infinitum until a match is found
- Create a faux-TMNT logo using http://glench.com/tmnt logic
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

### Caveats

I'm not developing this for anyone but myself, so you may see some anti-patterns like hardcoded paths specific to my environment, and general lack of configurability outside editing the source.

Given this runs once per hour, I'm not very concerned about performance. I often choose slow, but readable and easy-to-implement solutions.

### TODO

TODO:
  - Re-implement screenshot
  - local glench webpage
  - More docstrings
  - better README
  - CLI arguments
  - use real file format for keys
  - refactor key fetching to be done once

Super bonus points:
  - CI
