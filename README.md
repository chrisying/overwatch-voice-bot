# Overwatch Voice Responses Reddit Bot

__My voice response bot has been banned from the main /r/Overwatch subreddit. I've made multiple appeals to the mods but they seem to believe that the bot is not a good fit for the community. If you wish to see this bot become a reality, please let the subreddit mods know.__

A Reddit bot that scrapes [/r/Overwatch](http://reddit.com/r/overwatch) for hero quotes and responds with the appropriate voice line.

This is a work in progress *and may have bugs*. Please report any issues to me!

Supported voice lines can be found at: https://docs.google.com/spreadsheets/d/1Vs5dwQDx1tEmXPzTYzbHgY9x4NQ2fVtdmzHNUYuTF9c/edit?usp=sharing. Remember to export as `mapping.tsv`.

## Interesting files:

* `main.py`: the main Python file, run by calling `python main.py`
* `mapping.tsv`: map from text to voice data and other info
* `requirements.txt`: install the requirements via `sudo pip install -r requirements.txt`
* `local_config.py`: (gitignore'd) contains local information

## TODO's:

* Add more voice lines from [here](http://overwatch.gamepedia.com/Category:Quotations))
* Add counter for voice line usage

