
import re
import json

import praw
import OAuth2Util

from local_config import *

# Public configs go here
SUBREDDIT = 'fc_bot_test'
MAPPING_FILE = 'mapping.json'
NONALPHANUM = re.compile('[\W_]+')


def load_mapping():
    return json.loads(open(MAPPING_FILE).read())

def ignore_comment(c):
    if c.author == USERNAME:
        return True

def normalize_string(s):
    # TODO: more sophisticated normalization
    return NONALPHANUM.sub('', s).lower()

def construct_reply(data):
    # TODO: boilerplate
    output = ''
    output += '[%s](%s)' % (data['line'], data['voice'])

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

    # Main loop, comment_stream infinitely yields new comments
    for c in praw.helpers.comment_stream(r, SUBREDDIT, limit=1, verbosity=0):
        if ignore_comment(c):
            continue

        normal = normalize_string(c.body)
        if normal in mapping:
            reply = construct_reply(mapping[normal])
            c.reply(reply)

if __name__ == '__main__':
    main()
