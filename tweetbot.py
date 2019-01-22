#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

# python-twitter from https://github.com/bear/python-twitter
import logging
import logging.config
import os
import queue
import threading
import twitter
from twython import Twython

log_config = os.path.join(os.path.dirname(__file__), 'logger.ini')
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger('twitter')


class TweetBot(threading.Thread):

    def __init__(self, creds, queue):
        '''
        Auth should be a dict with twitter API credentials
        that have been imported from a .env or shell environment
        '''
        self.creds = creds
        self.queue = queue
        if self.creds:
            try:
                print('trying api')
                self.api = twitter.Api(creds)
            except Exception as e:
                print(e)
                # logger.error(e)
        # else:
            # logger.warn('No Twitter API Credentials')
        super().__init__()

    def watch(q):
        '''
        Accept Queue object as argument, interperet subscription info
        and assing to TweetBot object properties
        '''
        pass

    def run(self):
        while True:
            try:
                w = self.queue.get(timeout=2)
                print(w)
            except queue.Empty:
                return


if __name__ == "__main__":
    pass
