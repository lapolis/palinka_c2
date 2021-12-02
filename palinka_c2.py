#!/usr/bin/env python3

import logging

from core.stash import Stash
from core.main_menu import MainMenu


from platform import python_version
from os import path, getcwd, makedirs

if python_version()[0:3] < '3.7':
    print('\n\nMake sure you have Python 3.7+ installed, quitting.\n\n')
    exit(1)

def main():
    ## remove flask logs
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    # to fix (disable ALL logs)
    log.setLevel(logging.DEBUG)
    log.disabled = False

    ## create folders
    cwd = getcwd()
    out_fold = path.join(cwd, 'stash')
    if not path.isdir(out_fold):
        makedirs(out_fold)
    dow_fold = path.join(cwd, 'downloads')
    if not path.isdir(dow_fold):
        makedirs(dow_fold)
    pay_fold = path.join(cwd, 'payloads')
    if not path.isdir(pay_fold):
        makedirs(pay_fold)

    # to fix - arg for project name
    db = Stash(path.join(out_fold, 'PROJECT_NAME_0.4' + '.db'))
    db.db_init()

    ### Testing menu - Switch to tabs!!
    mm = MainMenu(db)
    mm.menu_init()
    
    exit(0)

if __name__ == '__main__':
    main()