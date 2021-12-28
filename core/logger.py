import logging
from os import system, name
from datetime import datetime
from colorama import Fore, Back, Style

# def write_logs(msg):
#     msg = 

def clear_screen():
    system('cls' if name == 'nt' else 'clear')

def error(msg,logger=False):
    # clear_screen()
    msg = f'\n\n       XX {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    if logger:
        logging.debug(msg)
    else:
        print( Fore.RED + msg + Style.RESET_ALL + Fore.RESET )
        input('       Enter to continue.')

def info(msg):
    # clear_screen()
    msg = f'\n\n       OO {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.BLUE + Style.DIM + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')

def warning(msg):
    # clear_screen()
    msg = f'\n\n       ## {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.YELLOW + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')

def success(msg):
    # clear_screen()
    msg = f'\n\n       ++ {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.GREEN + Style.BRIGHT + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')