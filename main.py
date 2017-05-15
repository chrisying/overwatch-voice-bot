
import logging
import re
import time

import praw
import unidecode

from local_config import *

# Public configs go here
MAPPING_FILE = 'mapping.tsv'
NORMALIZE_REGEX = re.compile('[^a-zA-Z0-9]')
COMMENT_TEMPLATE = '''
[%s](%s) (Sound warning: %s)

-----

^^Bleep ^^Bloop! ^^I ^^am ^^a ^^bot! ^^Report ^^issues ^^by ^^directly ^^messaging ^^me.

[^^Github](https://github.com/chrisying/overwatch-voice-bot) [^^Supported ^^lines](https://github.com/chrisying/overwatch-voice-bot/blob/master/mapping.tsv)
'''
ERROR_LIMIT = 10
logging.basicConfig(level=logging.INFO)

def load_mapping():
    # Parses mapping file as tsv
    # Format: first line is headers (ignore)
    # Following lines: normalized\thero\toriginal\texact\tvoice
    # Note: this function reads mapping.tsv as UTF-8 but PRAW reads comments as unicode
    mapping = {}
    with open(MAPPING_FILE) as f:
        f.readline()    # Read and ignore header
        for line in f.xreadlines():
            toks = line.split('\t')
            key = toks[0].replace(' ', '')
            mapping[key] = {
                    'hero': toks[1],
                    'line': toks[2],
                    'voice': toks[4]
            }
            if toks[3]:
                mapping[toks[2]] = {
                        'hero': toks[1],
                        'line': toks[2],
                        'voice': toks[4]
                }
    return mapping

def ignore_comment(comment):
    # Ignore certain comments without even looking at content
    # TODO: blacklist of people
    if str(comment.author) == USERNAME:
        return True

def normalize_string(s):
    # Converts unicode to ASCII, removes punctuation from string, lowercases
    # Input must be unicode
    asci = unidecode.unidecode(s)
    alpha = NORMALIZE_REGEX.sub('', asci)
    lower = alpha.lower()
    return lower

class VoiceLineBot:

    def __init__(self):
        logging.log(logging.INFO, 'Starting up bot.....')

        # Load mapping configuration before launching bot
        logging.log(logging.INFO, 'Loading mappings.....')
        self.mapping = load_mapping()
        logging.log(logging.INFO, 'Finished loading mappings.')

        # Initialize Reddit API
        logging.log(logging.INFO, 'Initializing and logging into %s.....' % USERNAME)
        self.reddit = praw.Reddit(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  password=PASSWORD,
                                  user_agent=USER_AGENT,
                                  username=USERNAME)
        logging.log(logging.INFO, 'Done initializing API.')

        logging.log(logging.INFO, 'Starting up comment stream in /r/%s.....' % SUBREDDIT)
        self.stream = self.reddit.subreddit(SUBREDDIT).stream.comments()

        # Ignore first 100 comments (could be historical)
        # TODO: if there are less than 100 comments, this blocks
        #for i in range(100):
        #    next(self.stream)

        logging.log(logging.INFO, 'Done initializing stream.')
        logging.log(logging.INFO, 'Parsing comments now:\n-----')

        self.total_counter = 0
        self.match_counter = 0

    def handle_comment(self, comment):
        # Handles responding or passing a comment
        self.total_counter += 1
        if self.total_counter % 100 == 0:
            logging.log(logging.INFO, 'Total comments: %d\tMatched comments: %d' % (self.total_counter, self.match_counter))

        comment_utf8 = comment.body.encode('utf-8')
        normal = normalize_string(comment.body)
        if comment_utf8 in self.mapping:
            comment_text = comment_utf8
        elif normal in self.mapping:
            comment_text = normal
        else:
            #logging.log(logging.INFO, 'Unmatched comment: %s' % comment.body)
            return

        logging.log(logging.INFO, 'Matched comment: %s' % comment.body)
        try:
            data = self.mapping[comment_text]
            reply = COMMENT_TEMPLATE % (data['line'], data['voice'], data['hero'])
            comment.reply(reply)
            logging.log(logging.INFO, 'Responded to comment: %s' % comment.body)
            self.match_counter += 1

            if self.match_counter % 10 == 0:
                logging.log(logging.INFO, 'Total comments: %d\tMatched comments: %d' % (self.total_counter, self.match_counter))
        except Exception as e:
            logging.log(logging.ERROR, 'Error replying to comment, %s: %s' % (e.__class__.__name__, e.message))


    def main_loop(self):
        # Main loop, stream infinitely yields new comments
        consecutive_errors = 0
        erroring = False
        while True:
            try:
                c = next(self.stream)
                erroring = False
            except Exception as e:
                logging.log(logging.ERROR, 'Error getting next comment, %s: %s' % (e.__class__.__name__, e.message))
                if erroring:
                    consecutive_errors += 1
                    if consecutive_errors >= ERROR_LIMIT:
                        sys.exit("Error limit reached, killing process")
                    time.sleep(consecutive_errors ** 2) # quadratic backoff
                else:
                    erroring = True
                    consecutive_errors = 1
                continue

            if ignore_comment(c):
                #logging.log(logging.INFO, 'Ignored comment: %s' % c.body)
                continue

            self.handle_comment(c)


def main():
    bot = VoiceLineBot()
    bot.main_loop()

if __name__ == '__main__':
    main()
