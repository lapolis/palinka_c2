#!/usr/bin/env python3

import re
import argparse
import datetime
import requests
import configparser

import logging
from core.mame import *
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
  log = logging.getLogger('mainLogs')
  log.disabled = False

  

if __name__ == '__main__':
  main()