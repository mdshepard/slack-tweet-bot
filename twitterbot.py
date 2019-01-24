#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

# python-twitter from https://github.com/bear/python-twitter
# import ipdb
import logging
import logging.config
import os
import queue
import threading
import twitter
from twython import Twython # noqa

log_config = os.path.join(os.path.dirname(__file__), 'logger.ini')
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger('twitter')


class TweetBot(threading.Thread):

    def __init__(self, creds, from_slack, to_slack):
        # ipdb.set_trace()
        '''
        Auth should be a dict with twitter API credentials
        that have been imported from a .env or shell environment
        '''
        print('In tweet bot\n{}'.format(from_slack.get()))
        self.creds = creds
        self.from_slack = from_slack
        self.to_slack = to_slack

        self.subs = {
            'users': [],
            'hashtags': [],
            'searchterms': []
        }

        if self.creds:
            self.APP_KEY = self.creds['consumer_key']
            self.APP_SECRET = self.creds['consumer_secret']
            self.OAUTH_TOKEN = self.creds['access_token_key']
            self.OAUTH_TOKEN_SECRET = self.creds['access_token_secret']
            try:
                logger.info('Connecting to Twitter API')
                self.api = twitter.Api(consumer_key=self.APP_KEY,
                                       consumer_secret=self.APP_SECRET,
                                       access_token_key=self.OAUTH_TOKEN,
                                       access_token_secret=self.OAUTH_TOKEN_SECRET) # noqa
                self.twy = Twython(self.APP_KEY, self.APP_SECRET,
                                   self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
                self.stream = ''
            except Exception as e:
                logger.error(e)
        else:
            logger.warn('No Twitter API Credentials')

        super().__init__()

    def watch(q):
        '''
        Accept Queue object as argument, interperet subscription info
        and assing to TweetBot object properties
        '''
        pass

    def get_user(self, user_id):
        '''
        Return twitter user info
        '''
        pass

    def get_status(self, status_id):
        '''
        Return twitter status
        '''
        return self.api

    def search_user(self, name):
        '''
        Search term and return results
        '''
        pass

    def run(self):
        while True:
            try:
                w = self.commands.get(timeout=2)
                print(w)
            except queue.Empty:
                return


if __name__ == "__main__":
    pass
