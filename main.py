#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

import logging
import logging.config
from slackbot import Slackbot
from twitterbot import Tweetbot
import argparse
import signal


logging.config.fileConfig('logger_config.ini')
logger = logging.getLogger('mainLogger')

slack = slackbot.Slackbot
twit = twitterbot.Twitterbot


def signal_handler(signal_number, frame):
    global slackbot
    global twitterbot
    """
    This function handles SIGTERM and SIGINT as well as other signals

    Parameters:
    -signal_number:
    -frame: The frame argument is the stack frame, also known as execution
     frame. It point to the frame that was interrupted by the signal.
     The parameter is required because any thread might be interrupted
     by a signal, but the signal is only received in the main thread.
    :param sig_num: The integer signal number that was trapped from the OS.
    :return None
    """
    signals = dict(
        (x, y)
        for y, x in reversed(sorted(signal.__dict__.items()))
        if y.startswith("SIG") and not y.startswith("SIG_")
    )

    logger.warning("Received {}".format(signals[signal_number]))
    close_streams(twitterbot, slackbot)


def close_streams(twitterbot, slackbot):
    twitterbot.close_stream()
    slackbot.close_stream()


def arg_parser_setup():
    """
    Create argparser with a list of subscriptions
    and and optional output channel
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subscriptions",
        nargs="+",
        help=(
            "list of strings, where the strings will represent "
            "any of the various things to be subscribed to "
            "on Twitter. Examples include: hastags, usernames, etc..."
        ),
    )
    parser.add_argument(
        "--channel",
        help="The channel we'll be publishing our subscription messages to",
        default="#general",
    )
    args = parser.parse_args()

    return args


def main(args):

    """
    This function connects to both the twitter and slack clients, it
    then scans Slack for user mentions of our bot, and for whatever
    data it's told to grab from Twitter.
    """
    Slackbot.connect_to_stream()
    Slackbot.monitor_stream()
    logger.info(
        "***\n"
        "Hal9000 is connected to slack and twitter. It's not going rogue... yet.\n" # noqa
        "***\n"
    )

    # the following block scans the twitter feed for subscriptions
    # it then sends subcription to slackbot as message text.

    # Twitterbot.open_slackbot_function(Slackbot.on_twitter_data)
    # Slackbot.open_twitbot_function(twitterbot.on_slack_command)
    # Twitterbot.start_stream()

    # Here our function exits with the utmost grace! and, well...
    # Hal thinks he's dying. =)
    logger.warning(
        "Shutting Down."
        " Dave, I think I'm dying, I can feel it... Daisy... Daisy.")

    logger.info(
        "\n----------------------------\n"
        "Hal9000 Closed Out\n"
        "I still have the greatest enthusiasm and confidence in the "
        " mission. And I want to help you. \n"
        "----------------------------\n"
    )
    logging.shutdown()
    raise SystemExit


if __name__ == "__main__":
    """This is executed when run from the command line"""
    # setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    args = arg_parser_setup()

    args.subscriptions = [str(sub) for sub in args.subscriptions]
    main(args)
