#!/bin/bash

# Run the TMNT bot.
#   Intended to be run by a cron job via a user's crontab, this script assumes
#   you have the source directory in ~/src/tmnt_wikipedia_bot, and that this
#   directory has a venv with all the requirements.txt packages, and that
#   ./src/keys.py has your API keys, and that the directories in
#   lib/constants.py match what are on your system. Also that your $HOME var is
#   set, and it helps if you have a ~/log directory.
#
#   It's not a good script, but I'm only building this for myself. :)
#
#                 "it works on my machine"

set -e

cd $HOME/src/tmnt_wikipedia_bot
. source ./bin/activate
python3 ./main.py &> $HOME/log/tmnt.log

