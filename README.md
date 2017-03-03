# Overwatch Voice Responses Reddit Bot

A Reddit bot that scrapes [/r/Overwatch](http://reddit.com/r/overwatch) for hero quotes and responds with the appropriate voice line.

This is currently in beta and is a work in progress. Feel free to send me a pull request if you want to contribute.

Supported voice lines can be found at: https://docs.google.com/spreadsheets/d/1Vs5dwQDx1tEmXPzTYzbHgY9x4NQ2fVtdmzHNUYuTF9c/edit?usp=sharing. Remember to export as `mapping.tsv`.

## Interesting files:

* `main.py`: the main Python file, run by calling `python main.py`
* `mapping.tsv`: map from text to voice data and other info
* `requirements.txt`: install the requirements via `sudo pip install -r requirements.txt`
* `local_config.py`: (gitignore'd) contains local information

## TODO's:

* Add more voice lines from [here](http://overwatch.gamepedia.com/Category:Quotations))
* Add an "special mappings" file that does exact matches for voice lines (handles things like D.Va's winky face and non-ASCII stuff)
* Figure out why the bot gets random HTTP 403's and gets stuck in exception loop
* Add counter for voice line usage
* Use [this](https://pypi.python.org/pypi/Unidecode) to decode unicode to ASCII for normalization

