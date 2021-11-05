
# use this one to capture someone pressing esc
# terminal_menu = TerminalMenu()
# if not terminal_menu.chosen_accept_key:
#	exit()

### temp import
import sys
sys.path.append('/home/blu/Documents/projectz/palinka_c2')
## delete!!

import os
import time
from core.stash import *
from simple_term_menu import TerminalMenu

class SubMenus :

    def __init__ (self, stash):
        self.stash = stash

        # general styling
        self.h_style = ('bg_green', 'fg_black', 'italics')
        self.h_kill_style = ('bg_red', 'italics')
        self.cursor = '       > '
        self.cursor_kill = '       X '
        self.cursor_style = ('fg_green', 'bold')
        self.cursor_style_kill = ('fg_red', 'bold')

    def listener_menu(self):
        ### Listeners main menu
        lmm_title = '\n\n       Listeners Menu\n'
        lmm_items = ['Show Listeners', 'Kill Listener', 'Back']
        lmm_back = False
        lmm = TerminalMenu(
            menu_entries=lmm_items,
            title=lmm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=True,
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
            clear_screen=True,
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
            clear_screen=True,
        )

        ## Listeners menu loop [0-2] ['Show Listeners', 'Kill Listener', 'Back']
        while not lmm_back:
            lmm_sel = lmm.show()

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
            
            elif lmm_sel == 2:
                lmm_back = True

    def main_menu(self):

        ### main menu
        mm_title = f'\n\n       Palinka C2 Main Menu\n'
        mm_items = ['Listeners', 'Agents', 'Overview', 'Quit']
        mm_exit = False

        mm = TerminalMenu(
            menu_entries=mm_items,
            title=mm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=True,
        )

        ## main menu loop [0-3] - ['Listeners', 'Agents', 'Overview', 'Quit']
        while not mm_exit:
            main_sel = mm.show()

            if main_sel == 0:
                ## Listeners menu loop
                self.listener_menu()

            elif main_sel == 1:
                print("Agent Menu Here!")
                time.sleep(2)

            elif main_sel == 2:
                print("Overview Menu Here!")
                time.sleep(2)

            elif main_sel == 3:
                mm_exit = True
                print("\n\n       Quitting!")

    def menu_init(self):
        self.main_menu()