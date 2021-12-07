from core.stash import *
from os import get_terminal_size
from colorama import Fore, Back, Style
from pynput.keyboard import Key, Listener

class LessPy :
    def __init__(self, info_string, stash):
        # Beacon Name - Listener - Remote IP - Hostname - Beacon Type
        self.a_name,self.l_name,self.ip,self.h_name,self.t_beacon = info_string.split(' - ')
        self.stash = stash

    def lessPy(self):
        full_list = self.gen_list(self.a_name, self.l_name)

        ### set key bindings!!!!

        self.currently_pressed_key = None
        with Listener( on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self,key):
        if key == self.currently_pressed_key:
            print('{0} repeated'.format(key))
        else:
            print('{0} pressed'.format(key))
            self.currently_pressed_key = key

    def on_release(self,key):
        self.currently_pressed_key = None
        if key == Key.esc:
            # Stop listener
            return False
   

    def gen_list(self, agent, listener):
        ret = [f'{Style.BRIGHT}Full command list fort aget {Fore.GREEN}{agent}{Fore.WHITE} connected to {Fore.GREEN}{listener}{Fore.WHITE}']
        high_comm = f'\n{Fore.GREEN}{Style.BRIGHT}Task - {Fore.WHITE}'
        high_resp = f'{Fore.CYAN}Result > '
        comms = self.stash.get_agents_comm_list(agent)
        ret.append('\n')
        for c in comms:
            cra = c[1].replace('\r','').split('\n')
            cr = cra[0]
            ret.append(f'{high_comm}{c[2]} {Fore.GREEN}>{Fore.WHITE} {c[0]}')
            if len(cra) > 1:
                ret.append(f'{high_resp}{cr}')
                for i in range(1,len(cra)):
                    if i != '' :
                        ret.append(f'{Fore.CYAN}{cra[i]}')
            else:
                ret.append(f'{high_resp}{Fore.RED}No response yet :({Style.RESET_ALL}')

        return ret

