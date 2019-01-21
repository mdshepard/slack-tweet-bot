#!/usr/bin/env python3
__author__ = 'mdshepard', 'mikaiyl', 'tjhindman',

# This needs to be from the python-dotenv package not dotenv
import dotenv


def get_dotenv():
    '''
    Reads .env file making API keys available
    '''
    return dotenv.dotenv_values()


if __name__ == "__main__":
    pass
