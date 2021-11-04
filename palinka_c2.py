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
from core.stash import Stash

from platform import python_version
from colorama import Fore, Back, Style
from os import system, path, getcwd, makedirs


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

from core.stash import *
def main():
    ## remove flask logs
    log = logging.getLogger('werkzeug')
    # to fix (disable ALL logs)
    # log.setLevel(logging.ERROR)
    log.disabled = False

    ## create folders
    cwd = getcwd()
    out_fold = path.join(cwd, 'stash')
    if not path.isdir(out_fold):
        makedirs(out_fold)
    dow_fold = path.join(cwd, 'downloads')
    if not path.isdir(dow_fold):
        makedirs(dow_fold)

    # to fix - arg for project name
    db = Stash(path.join(out_fold, 'PROJECT_NAME' + '.db'))
    db.db_init()


    listeners = OrderedDict()
    # listeners[name] = Listener(name, port, ipaddress)
    # listeners[name].start()

    listeners['list_one'] = HTTP_listener('main_listener_lol', '192.168.0.28', 9090, db)
    listeners['list_one'].start()

    input('stop one')
    listeners['list_one'].stop()

if __name__ == '__main__':
    main()