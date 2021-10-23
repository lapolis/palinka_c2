from datetime import datetime
from colorama import Fore, Back, Style

def error(msg):
    msg = f'XX {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.RED + msg + Style.RESET_ALL + Fore.RESET )

def info(msg):
    msg = f'OO {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.BLUE + Style.DIM + msg + Style.RESET_ALL + Fore.RESET )

def warning(msg):
    msg = f'## {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.YELLOW + msg + Style.RESET_ALL + Fore.RESET )

def success(msg):
    msg = f'++ {datetime.now().strftime("%H:%M:%S")} --> {msg}'
    print( Fore.GREEN + Style.BRIGHT + msg + Style.RESET_ALL + Fore.RESET )