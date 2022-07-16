#!/usr/bin/env python3

import string
import logging
import argparse
from getpass import getpass
from shutil import copyfile
from platform import python_version
from os import path, getcwd, makedirs, remove
from pyAesCrypt import encryptFile,decryptFile

from core.logger import *
from core.stash import Stash
from core.main_menu import MainMenu

def check_db(db_file):
    with open(db_file,'rb') as dbr:
        cleartext = dbr.read()
    if cleartext[0:15] == b'\x53\x51\x4c\x69\x74\x65\x20\x66\x6f\x72\x6d\x61\x74\x20\x33':
        return True
    else:
        False

def main():
    if python_version()[0:4] < '3.7':
        print('\n\nMake sure you have Python 3.7+ installed, quitting.\n\n')
        exit(1)

    p = argparse.ArgumentParser(description='Welcome to palinka_c2')
    p.add_argument('-f', '--file_name', default='palinka_c2_project', help='This name will be used to create the DB with all the logs and information. Letters, numbers and . _ only.')
    p.add_argument('-d', '--debug', action='store_true', default=False, help='Activate debugging. Everything will be saved in the file ./debug.log.')
    p.add_argument('-p', '--password', action='store_true', default=False, help='Encrypt DB with password. Password will be asked later.')
    p.add_argument('-j', '--just_decrypt', default='', help='Just decrypt the DB file and save on disk.')
    args = p.parse_args()
    
    ## create folders
    cwd = getcwd()
    out_fold = path.join(cwd, 'stash')
    if not path.isdir(out_fold):
        makedirs(out_fold)
    dow_fold = path.join(cwd, 'downloads')
    if not path.isdir(dow_fold):
        makedirs(dow_fold)
    up_fold = path.join(cwd, 'uploads')
    if not path.isdir(up_fold):
        makedirs(up_fold)
    pay_fold = path.join(cwd, 'payloads')
    if not path.isdir(pay_fold):
        makedirs(pay_fold)

    if args.debug:
        logging.basicConfig(filename='debug.log',level=logging.DEBUG)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.DEBUG)
        log.disabled = False
    else:
        log = logging.getLogger('werkzeug')
        log.disabled = True

    if args.password or args.just_decrypt:
        passwd = getpass( prompt='DB passwd: ' )
    else:
        passwd = None

    if args.just_decrypt:
        name = args.just_decrypt
    elif args.file_name:
        name = args.file_name
    else:
        error('I guess you did not input any project name?')
        exit(1)

    valid_chars = f'._{string.ascii_letters}{string.digits}'
    myName = ''.join(c for c in name if c in valid_chars)
    db_file = path.join(out_fold, myName + '.db')
    dec_db_file = path.join(out_fold, '.' + myName + '.db')
    new_flag = True

    if args.just_decrypt:
        if not path.isfile(db_file):
            error('That project does not exist.')
            exit(1)
        else:
            if check_db(db_file):
                error('That file is not encrypted.')
                exit(1)
            else:
                just_dec_db_file = path.join(out_fold, 'decrypted_' + myName + '.db')
                try:
                    decryptFile(db_file,just_dec_db_file,passwd)
                    success(f'File decrypted --> {just_dec_db_file}')
                except:
                    error('Wrong passwd or corrupted file.')
                    exit(1)

                if not check_db(just_dec_db_file):
                    error('Wrong passwd.')
                    remove(just_dec_db_file)
                    exit(1)
        exit(0)


    if path.isfile(db_file):
        if not check_db(db_file):
            if passwd:
                new_flag = False
                try:
                    decryptFile(db_file,dec_db_file,passwd)
                except:
                    error('Wrong passwd or corrupted file.')
                    exit(1)

                if not check_db(dec_db_file):
                    error('Wrong passwd.')
                    remove(dec_db_file)
                    exit(1)

                db = Stash(dec_db_file)
            else:
                error('This DB is encrypted, you must supply -p so you will be prompted for password.')
                exit(1)
        else:
            db = Stash(db_file)
    else:
        db = Stash(db_file)

    db.db_init()

    ### Testing menu - Switch to tabs!!
    mm = MainMenu(db,args.debug)
    mm.menu_init()

    if passwd:
        if new_flag:
            copyfile(db_file, dec_db_file)
        encryptFile(dec_db_file,db_file,passwd)
        l = path.getsize(dec_db_file)
        with open(dec_db_file,'wb') as dbw:
            dbw.write(b'\x00'*l)
        with open(dec_db_file,'wb') as dbw:
            dbw.write(b'\xff'*l)
        with open(dec_db_file,'wb') as dbw:
            dbw.write(b'\xAF'*l)
        remove(dec_db_file)

    
    exit(0)

if __name__ == '__main__':
    main()
