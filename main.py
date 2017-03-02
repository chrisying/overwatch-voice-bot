
import logging
import re
import time

import praw
#import OAuth2Util

from local_config import *

# Public configs go here
MAPPING_FILE = 'mapping.tsv'
NORMALIZE_REGEX = re.compile('[^a-zA-Z0-9 ]')
COMMENT_TEMPLATE = '''
[%s](%s) (Sound warning: %s)

-----

^I ^am ^a ^bot! ^Check ^out ^out ^my ^source ^code ^on [^Github](https://github.com/chrisying/overwatch-voice-bot)^! ^I ^am ^still ^in ^beta, ^please ^report ^issues ^by ^messaging ^me ^directly!
'''
logging.basicConfig(level=logging.INFO)

def load_mapping():
    # Parses mapping file as tsv
    # Format: first line is headers (ignore)
    # Following lines: normalized\thero\toriginal\tvoice
    mapping = {}
    with open(MAPPING_FILE) as f:
        f.readline()    # Read and ignore header
        for line in f.xreadlines():
            toks = line.split('\t')
            mapping[toks[0]] = {
                    'hero': toks[1],
                    'line': toks[2],
                    'voice': toks[3]
            }
    return mapping

def ignore_comment(comment):
    # Ignore certain comments without even looking at content
    # TODO: blacklist of people
    if str(comment.author) == USERNAME:
        return True

def normalize_string(s):
    # Removes punctuation from string and lowercases
    # TODO: create "special mappings" file which includes punctuation based
    #       voice lines like D.Va's ;) emote
    # TODO: consider removing spaces as well?
    return NORMALIZE_REGEX.sub('', s).lower()

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

        logging.log(logging.INFO, 'Starting up comment stream.....')
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
        normal = normalize_string(comment.body)
        if normal in self.mapping:
            logging.log(logging.INFO, 'Matched comment: %s' % comment.body)
            try:
                data = self.mapping[normal]
                reply = COMMENT_TEMPLATE % (data['line'], data['voice'], data['hero'])
                comment.reply(reply)
                logging.log(logging.INFO, 'Responded to comment: %s' % comment.body)
                self.match_counter += 1
            except Exception as e:
                print 'Error: %s' % e
                #logging.log(logging.INFO, 'Got RateLimitExceeded, sleeping for %d seconds' % e.sleep_time)
                #time.sleep(e.sleep_time)
        else:
            #logging.log(logging.INFO, 'Unmatched comment: %s' % c.body)
            pass

        self.total_counter += 1
        if self.total_counter % 100 == 0:
            logging.log(logging.INFO, 'Total comments considered: %d' % self.total_counter)
        if self.match_counter % 10 == 0:
            logging.log(logging.INFO, 'Matched comments: %d' % self.match_counter)

    def main_loop(self):
        # Main loop, stream infinitely yields new comments
        for c in self.stream:
            if ignore_comment(c):
                #logging.log(logging.INFO, 'Ignored comment: %s' % c.body)
                continue

            self.handle_comment(c)


def main():
    bot = VoiceLineBot()
    bot.main_loop()

if __name__ == '__main__':
    main()
