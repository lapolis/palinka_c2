from datetime import datetime
from colorama import Fore, Back, Style

# def write_logs(msg):
#     msg = 

def error(msg):
    msg = f'\n\n       XX {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.RED + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')

def info(msg):
    msg = f'\n\n       OO {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.BLUE + Style.DIM + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')

def warning(msg):
    msg = f'\n\n       ## {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.YELLOW + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')

def success(msg):
    msg = f'\n\n       ++ {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.GREEN + Style.BRIGHT + msg + Style.RESET_ALL + Fore.RESET )
    input('       Enter to continue.')