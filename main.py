#!/usr/bin/env python3
"""
Main function should tie in Slack API and Twitter API functionality
to determine which accounts to subscribe to and print some statistics
(i.e. total uptime, tweets recieved per minute, most frequent tweet
source, etc.). Should be enabled and disabled, but continue to count traffic.
"""

__author__ = 'mdshepard', 'mikaiyl', 'tjhindman'


import sys
import logging
import logging.config
import argparse
import signal
from slackbot import slackbot
from twitterbot import twitterbot


logging.config.fileConfig("logger.ini")
logger = logging.getLogger("mainLogger")
exit_flag = False


def signal_handler(sig, stack):
    """Recieves runtime errors to let you know when things are F.U.B.A.R."""

    logger.warn('Received ' + signal.Signals(sig).stack)
    exit_flag = True

    # Stream exit function from twitter and slack bout imports.
    twitterbot.close_stream()
    slackbot.close_stream()


def create_parser():
    """Creates and returns an argparse cmd line option parser"""

    parser = argparse.ArgumentParser(description="Perform transformation on input text.")
    parser.add_argument("subs", help="Specifies Twitter handle to be watched by program.")
    parser.add_argument("--channel", help="Specifies Slack channel for notifications to be posted in.")

    return parser


def main(args):
    """Implementation of Slack and Twitter modules."""

    logger.info(
        "----------------------------"
        "Hal9000 has powered on."
        "----------------------------")

    args = create_parser().parse_args(args)

    while not exit_flag:
        with Twitterbot(username="mikaiyl_twitterbot", subs=args.subs) as twitterbot:
            with Slackbot("Hal9000", args.channel) as slackbot:
                # Code inside of these function calls should call
                # the slackbot and twitterbot functions with monkey
                # chaining and start twitterbot and slackbot streams.

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


if __name__ == "__main__":
    """This is executed when run from the command line"""

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main(sys.argv[1:])
