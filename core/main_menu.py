
# use this one to capture someone pressing esc
# terminal_menu = TerminalMenu()
# if not terminal_menu.chosen_accept_key:
#   exit()

### temp import
import sys
sys.path.append('/home/blu/Documents/projectz/palinka_c2')
## delete!!

import os
import time
from core.stash import *
# from pynput import keyboard
from simple_term_menu import TerminalMenu

# from pynput import keyboard
from os import popen, system
# from core.sub_menu import SubMenus
from colorama import Fore, Back, Style

class MainMenu :
    def __init__(self, stash):
        self.stash = stash

        # general styling
        self.h_style = ('bg_green', 'fg_black', 'italics')
        self.h_kill_style = ('bg_red', 'italics')
        self.cursor = '       > '
        self.cursor_kill = '       X '
        self.cursor_style = ('fg_green', 'bold')
        self.cursor_style_kill = ('fg_red', 'bold')

        self.index = 0
        self.menu_entry = ['Listeners', 'Agents', 'Overview', 'Quit']

    def on_activate_r(self):
        self.index = (self.index + 1) % (len(self.menu_entry))
        self.print_menu()
    def on_activate_l(self):
        self.index = (self.index - 1) % (len(self.menu_entry))
        self.print_menu()

    def print_menu(self):
        system('clear')
        rows, columns = popen('stty size', 'r').read().split()
        # print(f'Rows {rows}')
        # print(f'Columns {columns}')

        slot = int(columns) / len(self.menu_entry)
        # rem = int(columns) % len(self.menu_entry)

        # print(len(self.menu_entry))
        # print(f'{slot}')
        print('''
 
  ██▓███   ▄▄▄       ██▓     ██▓ ███▄    █  ██ ▄█▀▄▄▄          ▄████▄    ██████ 
 ▓██░  ██▒▒████▄    ▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒▒████▄       ▒██▀ ▀█        ██▒ 
 ▓██░ ██▓▒▒██  ▀█▄  ▒██░    ▒██▒▓██  ▀█ ██▒▓███▄░▒██  ▀█▄     ▒▓█    ▄    ▄██▓▒   
 ▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██░    ░██░▓██▒  ▐▌██▒▓██ █▄░██▄▄▄▄██    ▒▓▓▄ ▄██▒ ▄█▓▒░
 ▒██▒ ░  ░ ▓█   ▓██▒░██████▒░██░▒██░   ▓██░▒██▒ █▄▓█   ▓██▒   ▒ ▓███▀ ░ ██████▒▒
 ▒██░ ░  ░ ▒▒   ▓▒█░░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒▒▒   ▓▒█░   ░ ░▒ ▒  ░ ▒ ▒▓▒ ▒ ░
 ░▓▒░       ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░ ▒   ▒▒ ░     ░  ▒    ░ ░▒  ░ ░
 ░▒         ░   ▒     ░ ░    ▒ ░   ░   ░ ░ ░ ░░ ░  ░   ▒      ░         ░  ░  ░  
  ░             ░  ░    ░  ░ ░           ░ ░  ░        ░  ░   ░ ░            ░  
                                                              ░                 
                                       
    ''')

        high = f'{Fore.WHITE}{Style.BRIGHT}{Back.GREEN}'
        low = f'{Fore.GREEN}{Back.WHITE}'
        menu_entry = [f'{" "*(int(slot/2)-3)}{e}{" "*(int(slot/2)-3)}' for e in self.menu_entry]
        menu_entry = [f'{high}{e}{Style.RESET_ALL}' if menu_entry[self.index] == e else f'{low}{e}{Style.RESET_ALL}' for e in menu_entry]
        print(f'{Fore.WHITE}{Style.BRIGHT}{Back.BLACK}|{Style.RESET_ALL}'.join(menu_entry))

        menu_to_show =  self.menu_entry[self.index]
        if menu_to_show == 'Listeners':
            self.listener_menu()
        elif menu_to_show == 'Agents':
            print('Agent Menu HERE!!')
            self.listener_menu()
        elif menu_to_show == 'Overview':
            print('Overview Menu HERE!!')
            self.listener_menu()
        elif menu_to_show == 'Quit':
            print('Quit Menu HERE!!')
            self.quit_menu()
        # self.sub_init()

    def menu_init(self):
        self.print_menu()

    ### sub menus

    def quit_menu(self):
        ### Listeners main menu
        qm_title = '\n\n       Are you sure???\n'
        qm_items = ['No!', 'No!', 'No!', 'Yes', 'No!', 'No!', 'No!']
        qm_back = False
        qm = TerminalMenu(
            menu_entries=qm_items,
            title=qm_title,
            menu_cursor=self.cursor_kill,
            menu_cursor_style=self.cursor_style_kill,
            menu_highlight_style=self.h_kill_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        while not qm_back:
            qm_sel = qm.show()

            if qm.chosen_accept_key == 'ctrl-w':
                self.on_activate_l()
                qm_back = True
            elif qm.chosen_accept_key == 'ctrl-e':
                qm_back = True
                self.on_activate_r()
            else:
                if qm_sel == 3:
                    system('clear')
                    qm_back = True




    def listener_menu(self):
        ### Listeners main menu
        lmm_title = '\n\n       Listeners Menu\n'
        # lmm_items = ['Show Listeners', 'Kill Listener', 'Back']
        lmm_items = ['Show Listeners', 'Kill Listener']
        lmm_back = False
        lmm = TerminalMenu(
            menu_entries=lmm_items,
            title=lmm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        ### Listeners List
        lm_list_title = '\n\n       Available Listeners\n'
        listeners = self.stash.get_listeners()
        if listeners:
            lm_list_items = [l[0] for l in listeners]
            lm_list_items.append('Back')
        else:
            lm_list_items = ['NO ACTIVE LISTENERS', 'Back']
        lm_list_back = False
        lm_list_menu = TerminalMenu(
            menu_entries=lm_list_items,
            title=lm_list_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        ### Listener Kill Menu
        ### use same items fo prev menu
        lm_kill_title = '\n\n       Listeners Killer\n'
        lm_kill_back = False
        lm_kill_menu = TerminalMenu(
            menu_entries=lm_list_items,
            title=lm_kill_title,
            menu_cursor=self.cursor_kill,
            menu_cursor_style=self.cursor_style_kill,
            menu_highlight_style=self.h_kill_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        # lmm_sel = lmm.show()

        # Listeners menu loop [0-2] ['Show Listeners', 'Kill Listener', 'Back']
        while not lmm_back:
            lmm_sel = lmm.show()

            if lmm.chosen_accept_key == 'ctrl-w':
                self.on_activate_l()
                lmm_back = True
            elif lmm.chosen_accept_key == 'ctrl-e':
                lmm_back = True
                self.on_activate_r()
            else:
                if lmm_sel == 0:
                    ## Listeners list menu
                    while not lm_list_back:
                        lm_list_sel = lm_list_menu.show()
                        if lm_list_items[lm_list_sel] == 'Back':
                            lm_list_back = True
                    
                    lm_list_back = False
                
                elif lmm_sel == 1:
                    ## kill listener menu
                    while not lm_kill_back:
                        lm_kill_sel = lm_kill_menu.show()
                        if lm_list_items[lm_kill_sel] == 'Back':
                            lm_kill_back = True
                    
                    lm_kill_back = False
                


    # def sub_init(self):
    #     self.main_sub()