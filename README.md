# Overwatch Voice Responses Reddit Bot

A Reddit bot that scrapes [/r/Overwatch](http://reddit.com/r/overwatch) for hero quotes and responds with the appropriate voice line.

This is currently in beta and is a work in progress. Feel free to send me a pull request if you want to contribute.

## Interesting files:

* `main.py`: the main Python file, run by calling `python main.py`
* `mapping.json`: map from text to voice data and other info
* `requirements.txt`: install the requirements via `sudo pip install -r requirements.txt`
* `local_config.py`: (gitignore'd) contains local information

## Known issues:

* `mapping.json` is incomplete (currently only some of Zenyatta, Zarya, and some ult lines), the source I'm pulling it from is incomplete :(
* The way I'm handling text normalization will not work for certain emotes (like D.Va's "Winky Face")
* Basically no error checking at all
* Eventually I will move the JSON file to a Google Sheet, and export to CSV

