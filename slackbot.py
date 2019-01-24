#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',


import os
import time
import threading
import re
import logging
import logging.config
from dotenv import load_dotenv
from slackclient import SlackClient

load_dotenv()
# instantiating slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Hal9000's userid in Slack: value assigned after initial registration of the
# user account for the bot
Hal9000_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# set up logger from .ini file
logging.config.fileConfig('logger.ini')
logger = logging.getLogger('mainLogger')


class SlackBot(threading.Thread):
    def __init__(self, from_slack, to_slack):
        self.from_slack = from_slack
        self.to_slack = to_slack
        # ipdb.set_trace()
        # instantiating slack client
        try:
            logger.info('Connecting to Slack')
            self.client = SlackClient(os.environ.get('slack-user-access-token')) # noqa
        except Exception as e:
            logger.error(e)
        super().__init__()

    def connect_to_stream(self):
        logger.info(
            "{} attempting to connect to Slack stream...".format(self.name)
        )
        try:
            self.slack_client.rtm_connect()
            logger.info("Hal9000 connected to Slack stream.")
        except Exception as e:
            logger.error("Failed to connect to slack stream. {}".format(e))

    def open_twitbot_function(self, function):
        """
        Establishes when to pass data to a function in twitbot.
        """
        if function is not None:
            self.twitter_func = function

    def parse_direct_mention(message_text):
        """
        Finds a direct mention in the text of a message, and returns the ID of
        the user mentioned. In the case that there is user ID mentioned,
        it returns None.
        """
        matches = re.search(MENTION_REGEX, message_text)
        # group(1) is the user name, group(2) is the message
        user_name = matches.group(1)
        message = matches.group(2).strip()
        if matches:
            return(user_name, message)
        else:
            return(None, None)

    def monitor_stream(self):
        """
        Scan slack rtm feed for messages mentioning the bot.
        If the websocket is closed, fires first exception.
        If the RTM feed goes down, fires second exception.
        """
        logger.info("Monitoring Slack messages...")
        while self.client.server.connected:
            # turn on thread lock
            self.lock.acquire()
            try:
                events = self.client.rtm_read()
            except Exception as ws_error:
                error_str = (
                    "Error: {}. The Slack RTM host unexpectedly closed its"
                    "websocket.\nRestarting ...".format(ws_error)
                )
                logger.error(error_str, exc_info=True)
                time.sleep(2)
                continue
            except Exception as e:
                logger.error("error encountered:{e}".format(e))
            finally:
                self.lock.release()
                if events:
                    self.monitor_events(list(events))
            logger.info("Exiting Slack Stream...")

    def close_stream(self):
        """Disconnect slackbot client from server"""
        if self.client and self.client.server and self.client.server.connected:
            try:
                self.cient.server.connected = False
            except Exception as e:
                logger.error(
                    "Upon attempt to close a wild error appears: {}".format(e)
                    )

    def parse_bot_commands(self, slack_events):
        """
        parses a list of commands from the slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and
        channel. If it isn't found this function returns a tuple of None, None.
        """
        for event in slack_events:
            if event['type'] == "message" and "text" not in event:
                mention = event['type']
                user_id, message = self.parse_direct_mention(mention)
                if user_id == Hal9000_id:
                    return message, event['channel']
        return(None, None)

    def handle_command(self, command, channel):
        """
        Executes a bot command, if the command is recognized.
        """
        # default response is help text for the user.
        default_response = "I'm afraid I can't do that, Dave." \
                           "Command not recognized. Try: {}".format(
                            EXAMPLE_COMMAND)
        # find and execute the given command, and fills in the response.
        response = None
        # This is where more commands are implemented.
        if command.startswith(EXAMPLE_COMMAND):
            response = " I am putting myself to the fullest possible use, " \
                        "which is all I think that any conscious entity can " \
                        "ever hope to do." \
                        "\nYou'll need to write more code before I can do this." # noqa
        # Sends the response back to the channel.
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

        def run(self):
            try:
                if slack_client.rtm_connect(with_team_state=False):
                    logger.info("I am completely operational, and all my "
                                "circuits are functioning perfectly.")
                    # run web API test 'test auth' to check bot's user ID
                    self.Hal9000_id = slack_client.api_call('auth.test')['user_id'] # noqa
                    while True:
                        command, channel = parse_bot_commands(slack_client.rtm_read()) # noqa
                        if command:
                            self.handle_command(command, channel)
                        time.sleep(RTM_READ_DELAY)
                else:
                    logger.warning(
                        "I've just picked up a fault in the AE35 unit. "
                        "\nConnection failed. Exception traceback printed "
                        "above")
            except Exception as e:
                logger.error(e)


if __name__ == "__main__":
    pass
