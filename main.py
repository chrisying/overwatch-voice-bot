
import json
import logging
import re
import time

import praw
#import OAuth2Util

from local_config import (
        USER_AGENT,
        USERNAME,
        PASSWORD,
        SUBREDDIT
)

# Public configs go here
CHUNK_SIZE = 10
MAPPING_FILE = 'mapping.json'
NORMALIZE_REGEX = re.compile('[^a-zA-Z0-9 ]')
COMMENT_TEMPLATE = '''
[%s](%s) (Sound warning: %s)

-----

^I ^am ^a ^bot! ^Check ^out ^out ^my ^source ^code ^on [^Github](https://github.com/chrisying/overwatch-voice-bot)^! ^I ^am ^still ^in ^beta, ^please ^report ^issues ^by ^messaging ^me ^directly!
'''
logging.basicConfig(level=logging.INFO)

def load_mapping():
    return json.loads(open(MAPPING_FILE).read())

def ignore_comment(c):
    if str(c.author) == USERNAME:
        return True

def normalize_string(s):
    # Removes punctuation from string and lowercases
    # TODO: create "special mappings" file which includes punctuation based
    # voice lines like D.Va's ;) emote
    return NORMALIZE_REGEX.sub('', s).lower()

def construct_reply(data):
    output = COMMENT_TEMPLATE % (data['line'], data['voice'], data['hero'])

    return output

def main():
    logging.log(logging.INFO, 'Starting up bot.....')

    # Load mapping configuration before launching bot
    logging.log(logging.INFO, 'Loading mappings.....')
    mapping = load_mapping()
    logging.log(logging.INFO, 'Finished loading mappings.')

    # Initialize Reddit API
    logging.log(logging.INFO, 'Initializing and logging into %s.....' % USERNAME)
    r = praw.Reddit(user_agent=USER_AGENT)
    r.login(username=USERNAME, password=PASSWORD, disable_warning=True)
    logging.log(logging.INFO, 'Done initializing API.')


    # TODO: eventually migrate to oauth, doesn't quite work yet
    #o = OAuth2Util.OAuth2Util(r)
    #o.refresh()

    logging.log(logging.INFO, 'Starting up comment stream.....')
    stream = praw.helpers.comment_stream(r, SUBREDDIT, limit=CHUNK_SIZE, verbosity=0)

    # Ignore first CHUNK_SIZE since they could be duplicate
    for i in range(CHUNK_SIZE):
        #print 'Ignored: ' + next(stream).body
        next(stream).body
    logging.log(logging.INFO, 'Done initializing stream.')
    logging.log(logging.INFO, 'Parsing comments now:\n-----')

    total_counter = 0
    match_counter = 0

    # Main loop, comment_stream infinitely yields new comments
    for c in stream:
        if ignore_comment(c):
            #logging.log(logging.INFO, 'Ignored comment: %s' % c.body)
            continue

        total_counter += 1
        normal = normalize_string(c.body)
        if normal in mapping:
            logging.log(logging.INFO, 'Matched comment: %s' % c.body)
            try:
                reply = construct_reply(mapping[normal])
                c.reply(reply)
                logging.log(logging.INFO, 'Responded to comment: %s' % c.body)
                match_counter += 1
            except praw.errors.RateLimitExceeded as e:
                logging.log(logging.INFO, 'Got RateLimitExceeded, sleeping for %d seconds' % e.sleep_time)
                time.sleep(e.sleep_time)
        else:
            #logging.log(logging.INFO, 'Unmatched comment: %s' % c.body)
            pass

        if total_counter % 100 == 0:
            logging.log(logging.INFO, 'Total comments considered: %d' % total_counter)


if __name__ == '__main__':
    main()
