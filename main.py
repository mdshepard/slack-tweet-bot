#!/usr/bin/env python3

"""
Main function should tie in Slack API and Twitter API functionality
to determine which accounts to subscribe to and print some statistics
(i.e. total uptime, tweets recieved per minute, most frequent tweet
source, etc.). Should be enabled and disabled, but continue to count traffic.
"""

__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

# This needs to be from the python-dotenv package not dotenv
import argparse
import dotenv
import logging
import logging.config
# import ipdb # noqa
import queue
import signal
import slackbot
import sys
import twitterbot

logging.config.fileConfig("logger.ini")
logger = logging.getLogger("mainLogger")
exit_flag = False


def get_dotenv():
    '''
    Reads .env file making API keys available
    '''
    return dotenv.dotenv_values()


def signal_handler(sig, stack):
    """Recieves runtime errors to let you know when things are F.U.B.A.R."""

    logger.warn('Received ' + signal.Signals(sig).name)

    global exit_flag
    exit_flag = True


def create_parser():
    """Creates and returns an argparse cmd line option parser"""
    parser = argparse.ArgumentParser(description="Perform transformation on input text.") # noqa
    # parser.add_argument("subs", help="Specifies Twitter handle to be watched by program.") # noqa
    # parser.add_argument("--channel", help="Specifies Slack channel for notifications to be posted in.") # noqa
    return parser


def main(args):
    """Implementation of Slack and Twitter modules."""

    logger.info(
        "----------------------------"
        "Hal9000 has powered on."
        "----------------------------")

    subs = queue.Queue()
    tweets = queue.Queue()

    sbot = slackbot.SlackBot(tweets, subs)
    # sbot.connect_to_stream()
    sbot.monitor_stream()
    sbot.start()

    tbot = twitterbot.TweetBot(get_dotenv(), subs, tweets)
    tbot.start()

    while not exit_flag:
        # ipdb.set_trace()
        pass

    subs.task_done()
    tweets.task_done()

    logger.warning("Shutting down... Daisy... Daisy...")
    logger.info(
        "----------------------------"
        "Hal9000 has left the building."
        "Processed {twitterbot_event_count} events"
        "in {twitterbot_runtime} minutes."
        "Detected an average of {twitterbot_tpm} tweets"
        "per minute."
        "The most frequent tweet source was {twitterbot_top_src}."
        "----------------------------"
    )

    logging.shutdown()
    raise SystemExit
    sys.exit()


if __name__ == "__main__":
    """This is executed when run from the command line"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    main(create_parser().parse_args())
