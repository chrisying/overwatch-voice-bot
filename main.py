
import json
import re

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

def load_mapping():
    return json.loads(open(MAPPING_FILE).read())

def ignore_comment(c):
    if c.author == USERNAME:
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
    # Load mapping configuration before launching bot
    mapping = load_mapping()

    # Initialize Reddit API
    r = praw.Reddit(user_agent=USER_AGENT)
    r.login(username=USERNAME, password=PASSWORD, disable_warning=True)

    # TODO: eventually migrate to oauth, doesn't quite work yet
    #o = OAuth2Util.OAuth2Util(r)
    #o.refresh()

    stream = praw.helpers.comment_stream(r, SUBREDDIT, limit=CHUNK_SIZE, verbosity=0)

    # Ignore first CHUNK_SIZE since they could be duplicate
    for i in range(CHUNK_SIZE):
        print 'Ignored: ' + next(stream).body

    # Main loop, comment_stream infinitely yields new comments
    for c in stream:
        if ignore_comment(c):
            continue

        normal = normalize_string(c.body)
        if normal in mapping:
            print 'Responded to comment: %s' % c
            reply = construct_reply(mapping[normal])
            c.reply(reply)

if __name__ == '__main__':
    main()
