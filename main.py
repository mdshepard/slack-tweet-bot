#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

# This needs to be from the python-dotenv package not dotenv
import dotenv
import queue
import tweetbot


def get_dotenv():
    '''
    Reads .env file making API keys available
    '''
    return dotenv.dotenv_values()


def main():
    '''
    Main function. Everything happens here.
    '''
    subs = queue.Queue()
    tweets = queue.Queue()

    twitbot = tweetbot.TweetBot(get_dotenv(), subs, tweets)


if __name__ == "__main__":
    main()
