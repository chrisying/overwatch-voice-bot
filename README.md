# Overwatch Voice Responses Reddit Bot

A Reddit bot that scrapes [/r/Overwatch](http://reddit.com/r/overwatch) for hero quotes and responds with the appropriate voice line.

This is currently in beta and is a work in progress. Feel free to send me a pull request if you want to contribute.

Supported Voice lines can be found at: https://docs.google.com/spreadsheets/d/1Vs5dwQDx1tEmXPzTYzbHgY9x4NQ2fVtdmzHNUYuTF9c/edit?usp=sharing. Remember to export as `mapping.tsv`.

## Interesting files:

* `main.py`: the main Python file, run by calling `python main.py`
* `mapping.tsv`: map from text to voice data and other info
* `requirements.txt`: install the requirements via `sudo pip install -r requirements.txt`
* `local_config.py`: (gitignore'd) contains local information

## Known issues:

* Have not gotten around to adding all lines (audio files can be found [here](http://overwatch.gamepedia.com/Category:Quotations))
* The way I'm handling text normalization will not work for certain emotes (like D.Va's "Winky Face")
* Basically no error checking at all

