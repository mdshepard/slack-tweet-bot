#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

import twitter
import logging
import logging.config

logging.config.fileConfig('logger_config.ini')
logger = logging.getLogger('twitter')


class TweetBot(object):

    def __init__(self, creds):
        '''
        Auth should be a dict with twitter API credentials
        that have been imported from a .env or shell environment
        '''
        if creds:
            try:
                self.api = twitter.Api(**creds)
            except Exception as e:
                logger.error(e)
        else:
            logger.warn('No Twitter API Credentials')

    def assign_queue(q):
        '''
        Accept Queue object as argument, interperet subscription info
        and assing to TweetBot object properties
        '''
        pass


if __name__ == "__main__":
    pass
