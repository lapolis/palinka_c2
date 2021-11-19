#!/usr/bin/env python3

import logging

## maybe not here???
from collections import OrderedDict

from core.stash import Stash
from core.main_menu import MainMenu
from core.listener import HTTP_listener

from platform import python_version
from os import system, path, getcwd, makedirs

# system('clear')

# if python_version()[0:3] < '3.7':
#     print('\n\nMake sure you have Python 3.7+ installed, quitting.\n\n')
#     exit(1)

# print('''

#  ██▓███   ▄▄▄       ██▓     ██▓ ███▄    █  ██ ▄█▀▄▄▄          ▄████▄    ██████ 
# ▓██░  ██▒▒████▄    ▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒▒████▄       ▒██▀ ▀█        ██▒ 
# ▓██░ ██▓▒▒██  ▀█▄  ▒██░    ▒██▒▓██  ▀█ ██▒▓███▄░▒██  ▀█▄     ▒▓█    ▄    ▄██▓▒   
# ▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██░    ░██░▓██▒  ▐▌██▒▓██ █▄░██▄▄▄▄██    ▒▓▓▄ ▄██▒ ▄█▓▒░
# ▒██▒ ░  ░ ▓█   ▓██▒░██████▒░██░▒██░   ▓██░▒██▒ █▄▓█   ▓██▒   ▒ ▓███▀ ░ ██████▒▒
# ▒▓▒░ ░  ░ ▒▒   ▓▒█░░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒▒▒   ▓▒█░   ░ ░▒ ▒  ░ ▒ ▒▓▒ ▒ ░
# ░▒ ░       ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░ ▒   ▒▒ ░     ░  ▒    ░ ░▒  ░ ░
# ░░         ░   ▒     ░ ░    ▒ ░   ░   ░ ░ ░ ░░ ░  ░   ▒      ░         ░  ░  ░  
#                ░  ░    ░  ░ ░           ░ ░  ░        ░  ░   ░ ░            ░  
#                                                              ░                 
                                      
#     ''')

def main():
    ## remove flask logs
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
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
    db = Stash(path.join(out_fold, 'PROJECT_NAME_0.1' + '.db'))
    db.db_init()



    listeners = OrderedDict()
    # listeners[name] = Listener(name, port, ipaddress)
    # listeners[name].start()

    listeners['first_listener'] = HTTP_listener('first_listener', '192.168.0.28', 9090, db)
    listeners['first_listener'].start()

    ### Testing menu - Switch to tabs!!
    mm = MainMenu(db)
    mm.menu_init()
    

    listeners['first_listener'].stop()
    exit(0)

if __name__ == '__main__':
    main()