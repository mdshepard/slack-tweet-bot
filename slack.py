#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'TJs github name',

import os
import time
import re
from slackclient import SlackClient

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
    pass


def handle_command(command, channel):
    pass


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print('Hal9000 connected and running')
        # Read bot's user ID by calling the Web API method 'auth test'
        Hal9000_id = slack_client.api_call('auth.test')['user_id']
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print('connection failed. exception traceback printed above')
