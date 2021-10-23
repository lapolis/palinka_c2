#!/usr/bin/env python3

import re
import argparse
import datetime
import requests
import configparser

from time import sleep

import logging
from core.mame import *

from collections import OrderedDict

from core.listener import HTTP_listener

from os import system, path
from platform import python_version
from colorama import Fore, Back, Style


# system('clear')

# if python_version()[0:3] < '3.7':
#     print('\n\nMake sure you have Python 3.7+ installed, quitting.\n\n')
#     exit(1)

# print('''

# █     █░▄▄▄█████▓  █████▒    ▄▄▄       ███▄ ▄███▓    ██▓   ▓█████▄  ▒█████   ██▓ ███▄    █   ▄████ 
# ▓█░ █ ░█░▓  ██▒ ▓▒▓██   ▒    ▒████▄    ▓██▒▀█▀ ██▒   ▓██▒   ▒██▀ ██▌▒██▒  ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒
# ▒█░ █ ░█ ▒ ▓██░ ▒░▒████ ░    ▒██  ▀█▄  ▓██    ▓██░   ▒██▒   ░██   █▌▒██░  ██▒▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
# ░█░ █ ░█ ░ ▓██▓ ░ ░▓█▒  ░    ░██▄▄▄▄██ ▒██    ▒██    ░██░   ░▓█▄   ▌▒██   ██░░██░▓██▒  ▐▌██▒░▓█  ██▓
# ░░██▒██▓   ▒██▒ ░ ░▒█░        ▓█   ▓██▒▒██▒   ░██▒   ░██░   ░▒████▓ ░ ████▓▒░░██░▒██░   ▓██░░▒▓███▀▒
# ░ ▓░▒ ▒    ▒ ░░    ▒ ░        ▒▒   ▓▒█░░ ▒░   ░  ░   ░▓      ▒▒▓  ▒ ░ ▒░▒░▒░ ░▓  ░ ▒░   ▒ ▒  ░▒   ▒ 
#   ▒ ░ ░      ░     ░           ▒   ▒▒ ░░  ░      ░    ▒ ░    ░ ▒  ▒   ░ ▒ ▒░  ▒ ░░ ░░   ░ ▒░  ░   ░ 
#   ░   ░    ░       ░ ░         ░   ▒   ░      ░       ▒ ░    ░ ░  ░ ░ ░ ░ ▒   ▒ ░   ░   ░ ░ ░ ░   ░ 
#     ░                              ░  ░       ░       ░        ░        ░ ░   ░           ░       ░ 
#                                                              ░                                      

#     ''')

def main():
    log = logging.getLogger('werkzeug')
    # to fix (disable ALL logs)
    # log.setLevel(logging.ERROR)
    log.disabled = False

    listeners = OrderedDict()

    # listeners[name] = Listener(name, port, ipaddress)
    # listeners[name].start()
    listeners['list_one'] = HTTP_listener('Flask_listener', '127.0.0.1', 9090)
    listeners['list_one'].start()

    input('stop one')
    listeners['list_one'].stop()

if __name__ == '__main__':
    main()