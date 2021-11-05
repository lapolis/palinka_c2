
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


def main():
    ### delete and fix
    db = Stash(path.join('/home/blu/Documents/projectz/palinka_c2', 'stash', 'PROJECT_NAME' + '.db'))
    db.db_init()
    ### delete and fix


    # general styling
    h_style = ('bg_green', 'fg_black', 'italics')
    cursor = '       > '
    cursor_style = ('fg_green', 'bold')

    # main menu
    mm_title = f'\n\n       Palinka C2 Main Menu\n'
    mm_items = ['Listeners', 'Agents', 'Overview', 'Quit']
    mm_exit = False

    main_menu = TerminalMenu(
        menu_entries=mm_items,
        title=mm_title,
        menu_cursor=cursor,
        menu_cursor_style=cursor_style,
        menu_highlight_style=h_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    lm_list_title = '\n\n       Available Listeners\n'
    listeners = db.get_listeners()
    print(listeners)
    if listeners:
        lm_list_items = [l[0] for l in listeners]
    else:
        lm_list_items = ['NO ACTIVE LISTENER']
    lm_list_back = False
    edit_menu = TerminalMenu(
        menu_entries=lm_list_items,
        title=lm_list_title,
        menu_cursor=cursor,
        menu_cursor_style=cursor_style,
        menu_highlight_style=h_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    while not mm_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not lm_list_back:
                edit_sel = edit_menu.show()
                if edit_sel == 0:
                    print("Edit Config Selected")
                    time.sleep(5)
                elif edit_sel == 1:
                    print("Save Selected")
                    time.sleep(5)
                elif edit_sel == 2:
                    lm_list_back = True
                    print("Back Selected")
            lm_list_back = False
        elif main_sel == 1:
            print("option 2 selected")
            time.sleep(5)
        elif main_sel == 2:
            print("option 3 selected")
            time.sleep(5)
        elif main_sel == 3:
            mm_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()