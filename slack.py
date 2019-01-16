#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

import logging
import os
import time
import re
from dotenv import load_dotenv
from slackclient import SlackClient

load_dotenv()
# instantiating slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Hal9000's userid in Slack: value is assigned after the bot starts up
Hal9000_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
    parses a list of commands from the slack RTM API to find bot commands.
    If a bot command is found, this function returns a tuple of command and
    channel. If it isn't found this function returns a tuple of None, None.
    """
    for event in slack_events:
        if event['type'] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event['text'])
            if user_id == Hal9000_id:
                return message, event['channel']
    return(None, None)


def parse_direct_mention(message_text):
    """
    Finds a direct mention (a message that is at the beginning of a message)
    in the text of a message, and returns the ID of the user mentioned. In
    the case that there is user ID mentioned, it returns None.
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains username, the second contains the remaining msg
    return (
        matches.group(1), matches.group(2).strip()
        ) if matches else (None, None)


def handle_command(command, channel):
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
                   "which is all I think that any conscious entity can ever " \
                   "hope to do." \
                   "\n You'll need to write more code before I can do this."

    # Sends the response back to the channel.
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    try:
        if slack_client.rtm_connect(with_team_state=False):
            print("I am completely operational, and all my "
                  "circuits are functioning perfectly.")
            # Read bot's user ID by calling the Web API method 'auth test'
            Hal9000_id = slack_client.api_call('auth.test')['user_id']
            while True:
                command, channel = parse_bot_commands(slack_client.rtm_read())
                if command:
                    handle_command(command, channel)
                time.sleep(RTM_READ_DELAY)
        else:
            print(
                "I've just picked up a fault in the AE35 unit. "
                "\nConnection failed. Exception traceback printed above")
    except Exception as e:
        print(e)
