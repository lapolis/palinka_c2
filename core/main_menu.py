
# use this one to capture someone pressing esc
# terminal_menu = TerminalMenu()
# if not terminal_menu.chosen_accept_key:
#   exit()

import readline
from time import time
from random import choice
from string import ascii_letters
from ipaddress import ip_address
from collections import OrderedDict
from simple_term_menu import TerminalMenu

from colorama import Fore, Back, Style
from os import popen, system, getcwd, name, get_terminal_size

from core.stash import *
from core.less import LessPy
from core.listener import HTTP_listener

class MainMenu :
    def __init__(self, stash, debug=False):
        ## testing
        self.quit = False

        self.stash = stash
        self.debug = debug

        # general styling
        self.h_style = ('bg_green', 'fg_black', 'italics')
        self.h_kill_style = ('bg_red', 'italics')
        self.cursor = '       > '
        self.cursor_kill = '       X '
        self.cursor_style = ('fg_green', 'bold')
        self.cursor_style_kill = ('fg_red', 'bold')

        self.index = 0
        self.menu_entry = ['Listeners', 'Agents', 'Overview', 'Quit']

        self.CMD = ['shell', 'powershell', 'sleep', 'rename', 'back_to_previous_menu']

        self.listener_types = ['HTTPS', 'HTTP', 'back']
        self.payloads_types = OrderedDict()
        # self.payloads_types['HTTPS'] = ['powershell', 'c++ (soon)']
        self.payloads_types['HTTPS'] = ['powershell']
        self.payloads_types['HTTP'] = ['powershell']

        self.listeners = OrderedDict()
        ## init listeners still alive
        full_list = self.stash.get_listeners(full=True)
        for ll in full_list:
            if ll[1] in ['HTTPS','HTTP']:
                self.listeners[ll[0]] = HTTP_listener(ll[1], ll[0], ll[2], ll[3], self.stash, self.debug)
                self.listeners[ll[0]].start()

    def clear_screen(self):
        system('cls' if name == 'nt' else 'clear')

    ### find a way to use only one function (text and state non existing error)
    def cmd_completer(self, text, state):
        options = [cmd for cmd in self.CMD if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else :
            return None

    def listener_completer(self, text, state):
        options = [cmd for cmd in self.listener_types if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else :
            return None

    def on_activate_r(self):
        self.index = (self.index + 1) % (len(self.menu_entry))
    def on_activate_l(self):
        self.index = (self.index - 1) % (len(self.menu_entry))

    def menu_banner(self, full=False):
        self.clear_screen()
        tsize = get_terminal_size()
        # rows, columns = popen('/usr/bin/stty size', 'r').read().split()
        columns, rows = tsize

        slot = int(columns) / len(self.menu_entry)
        if full:
            print('''
 
  ██▓███   ▄▄▄       ██▓     ██▓ ███▄    █  ██ ▄█▀▄▄▄          ▄████▄   ░██████ 
 ▓██░  ██▒▒████▄    ▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒▒████▄       ▒██▀ ▀█    ░   ██▒ 
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

    def print_menu(self):
 #        self.clear_screen()
 #        tsize = get_terminal_size()
 #        # rows, columns = popen('/usr/bin/stty size', 'r').read().split()
 #        columns, rows = tsize

 #        slot = int(columns) / len(self.menu_entry)
 #        print('''
 
 #  ██▓███   ▄▄▄       ██▓     ██▓ ███▄    █  ██ ▄█▀▄▄▄          ▄████▄   ░██████ 
 # ▓██░  ██▒▒████▄    ▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒▒████▄       ▒██▀ ▀█    ░   ██▒ 
 # ▓██░ ██▓▒▒██  ▀█▄  ▒██░    ▒██▒▓██  ▀█ ██▒▓███▄░▒██  ▀█▄     ▒▓█    ▄    ▄██▓▒   
 # ▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██░    ░██░▓██▒  ▐▌██▒▓██ █▄░██▄▄▄▄██    ▒▓▓▄ ▄██▒ ▄█▓▒░
 # ▒██▒ ░  ░ ▓█   ▓██▒░██████▒░██░▒██░   ▓██░▒██▒ █▄▓█   ▓██▒   ▒ ▓███▀ ░ ██████▒▒
 # ▒██░ ░  ░ ▒▒   ▓▒█░░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒▒▒   ▓▒█░   ░ ░▒ ▒  ░ ▒ ▒▓▒ ▒ ░
 # ░▓▒░       ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░ ▒   ▒▒ ░     ░  ▒    ░ ░▒  ░ ░
 # ░▒         ░   ▒     ░ ░    ▒ ░   ░   ░ ░ ░ ░░ ░  ░   ▒      ░         ░  ░  ░  
 #  ░             ░  ░    ░  ░ ░           ░ ░  ░        ░  ░   ░ ░            ░  
 #                                                              ░                 
                                       
 #    ''')

        # high = f'{Fore.WHITE}{Style.BRIGHT}{Back.GREEN}'
        # low = f'{Fore.GREEN}{Back.WHITE}'
        # menu_entry = [f'{" "*(int(slot/2)-3)}{e}{" "*(int(slot/2)-3)}' for e in self.menu_entry]
        # menu_entry = [f'{high}{e}{Style.RESET_ALL}' if menu_entry[self.index] == e else f'{low}{e}{Style.RESET_ALL}' for e in menu_entry]
        # print(f'{Fore.WHITE}{Style.BRIGHT}{Back.BLACK}|{Style.RESET_ALL}'.join(menu_entry))
        self.menu_banner(full=True)
        menu_to_show =  self.menu_entry[self.index]
        if menu_to_show == 'Listeners':
            self.listener_menu()
        elif menu_to_show == 'Agents':
            self.agents_menu()
        elif menu_to_show == 'Overview':
            overview_item = self.overview_menu()
            if overview_item:
                # success(f'WTF {overview_item}')
                less = LessPy(overview_item, self.stash)
                less.lessPy()
        elif menu_to_show == 'Quit':
            self.quit_menu()

    def menu_init(self):
        while not self.quit:
            self.print_menu()

    def quit_menu(self):
        ### Listeners main menu
        qm_title = '\n\n       Are you sure???\n'
        qm_items = ['No!', 'No!', 'No!', 'Yes', 'No!', 'No!', 'No!']
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

        qm_sel = qm.show()
        if qm.chosen_accept_key == 'ctrl-w':
            self.on_activate_l()
        elif qm.chosen_accept_key == 'ctrl-e':
            self.on_activate_r()
        else:
            if qm_sel == 3:
                self.quit = True
                self.clear_screen()

    def agent_list_gen(self):
        ### Agents List
        agents = self.stash.get_agents()
        if agents:
            agent_list = [f'Agent: {a[0]} @ {a[1]} --> listener: {a[2]}' for a in agents]
            agent_list.append('Back')
        else:
            agent_list = ['NO ACTIVE AGENTS, you n00b', 'Back']
        return agent_list

    def agents_menu(self):
        ### Agents main menu
        amm_title = '\n\n       Agents Menu\n'
        amm_items = ['Show Agents', 'Kill Agent']
        amm = TerminalMenu(
            menu_entries=amm_items,
            title=amm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        am_list_title = '\n\n       Select Aget to Interact\n'
        am_list_items = self.agent_list_gen()
        am_list_back = False
        am_list_menu = TerminalMenu(
            menu_entries=am_list_items,
            title=am_list_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w'),
            preview_command=self.short_com_hist,
            preview_size=0.60,
            preview_title=f'{Style.BRIGHT}Short Commands History{Style.RESET_ALL}'
        )

        am_kill_title = '\n\n       Agents Killer\n'
        am_kill_menu = TerminalMenu(
            menu_entries=am_list_items,
            title=am_kill_title,
            menu_cursor=self.cursor_kill,
            menu_cursor_style=self.cursor_style_kill,
            menu_highlight_style=self.h_kill_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        amm_sel = amm.show()
        if amm.chosen_accept_key == 'ctrl-w':
            self.on_activate_l()
        elif amm.chosen_accept_key == 'ctrl-e':
            self.on_activate_r()
        else:
            
            if amm_sel == 0:
                ## agents list menu
                # find a way to regenerate agent list
                while not am_list_back:
                    self.menu_banner()
                    am_list_sel = am_list_menu.show()
                    if am_list_menu.chosen_accept_key == 'ctrl-w':
                        am_list_back = True
                        self.on_activate_l()
                    elif am_list_menu.chosen_accept_key == 'ctrl-e':
                        am_list_back = True
                        self.on_activate_r()
                    else:
                        if am_list_items[am_list_sel] not in ['Back', 'NO ACTIVE AGENTS, you n00b']:
                            task_input = self.get_task_input(am_list_items[am_list_sel].split()[1])
                        else:
                            am_list_back = True

            elif amm_sel == 1:
                ## kill agent menu
                am_kill_sel = am_kill_menu.show()

                if am_kill_menu.chosen_accept_key == 'ctrl-w':
                    self.on_activate_l()
                elif am_kill_menu.chosen_accept_key == 'ctrl-e':
                    self.on_activate_r()
                else:
                    if am_list_items[am_kill_sel] not in ['Back', 'NO ACTIVE AGENTS, you n00b']:
                        agent = am_list_items[am_kill_sel].split()[1]
                        command_code = self.gen_command_code()
                        cmd = 'quit'
                        self.stash.set_agent_job(command_code, agent, cmd)
                        self.stash.sql_stash( 'UPDATE agents SET alive = ? WHERE agent_name = ? ;', (False, agent) )

    def get_task_input(self, agent):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.cmd_completer)
        header = f'\n\n       Set Task to {agent}. Tab is your friend.'
        cmd = ''
        while cmd == '' or cmd.split()[0] not in self.CMD:
            cmd = input(f'{header}\n{Fore.GREEN}{Style.BRIGHT}{self.cursor}{Style.RESET_ALL}')
        if 'back_to_previous_menu' not in cmd:
            command_code = self.gen_command_code()
            self.stash.set_agent_job(command_code, agent, cmd)

    def gen_command_code(self):
        command_code = ''.join(choice(ascii_letters) for i in range(10))
        comms = self.stash.get_command_codes()
        if comms:
            comms_list = [c[0] for c in comms]
        else:
            comms_list = []
        while command_code in comms_list:
            command_code = ''.join(choice(ascii_letters) for i in range(10))
        return command_code

    def short_com_hist(self, agent):
        if agent == 'Back':
            return '\nGoing back?\n'
        high_comm = f'{Fore.GREEN}{Style.BRIGHT} Task - {Fore.WHITE}'
        high_resp = f'{Fore.CYAN} Result > '
        comms = self.stash.get_agents_comm_list(agent.split()[1])
        ret = '\n'
        for c in comms:
            cra = c[1].replace('\r','').split('\n')
            cr = cra[0]
            if len(cra) > 1:
                # cr = ''.join([f'{" "*11}{Fore.CYAN}{cc}\n' for cc in cra])
                for i in range(1,len(cra)):
                    cr += f'{" "*10}{Fore.CYAN}{cra[i]}\n'
            ret += f'{high_comm}{c[2]} {Fore.GREEN}>{Fore.WHITE} {c[0]}\n{high_resp}{cr}{Style.RESET_ALL}\n'
        return ret

    def listener_preview(self, listener_entry):
        if listener_entry in ['NO ACTIVE LISTENERS', 'Back']:
            return '\nGoing back?\n'

        name = f'{Style.BRIGHT}{Fore.GREEN}'
        val = f'{Style.BRIGHT}{Fore.CYAN}'
        ln = listener_entry.split()[-1]
        listener = self.stash.get_listener(ln)[0]
        agents_list = self.stash.get_agents(ln)
        if agents_list == []:
            agents = 'None you n00b!'
        else:
            agents = f'{agents_list[0][0]} - {agents_list[0][1]}'
            if len(agents_list) > 1:
                for a in agents_list:
                    agents += f'\n{val}        {a[0]} - {a[1]}'

        ret = '\n'
        if listener[0] in ['HTTPS','HTTP']:
            ret += f'{name}Listener Type: {val}{listener[0]}\n'
            ret += f'{name}Listener Name: {val}{ln}\n'
            ret += f'{name}Listening IP: {val}{listener[1]}\n'
            ret += f'{name}Listening Port: {val}{listener[2]}\n'
            ret += f'{name}Agents: {val}{agents}'
        ret += f'{Style.RESET_ALL}\n'
        return ret

    def overview_menu(self):
        ### Overview main menu
        omm_title = '\n\n       Overview - enter to get more info\n'
        ## generate big ass list with all info
        items = self.stash.get_agents(full=True)
        if items:
            omm_items = ['Beacon Name - Listener - Remote IP - Hostname - Beacon Type']
        else:
            omm_items = ['Throw some agents around you n00b!']

        for i in items:
            omm_items.append(f'{i[0]} - {i[1]} - {i[2]} - {i[3]} - {i[4]}')

        omm = TerminalMenu(
            menu_entries=omm_items,
            title=omm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )
        omm_sel = omm.show()

        if omm.chosen_accept_key == 'ctrl-w':
            self.on_activate_l()
        elif omm.chosen_accept_key == 'ctrl-e':
            self.on_activate_r()
        else:
            if omm_sel != 0:
                self.clear_screen()
                return omm_items[omm_sel]
            else:
                return None

    def listener_menu(self):
        ### Listeners main menu
        lmm_title = '\n\n       Listeners Menu\n'
        lmm_items = ['Show Listeners', 'New Listener', 'Kill Listener']
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
        lm_list_title = '\n\n       Available Listeners - Press enter while a listener is highlighted to generate the payload\n'
        listeners = self.stash.get_listeners()
        if listeners:
            lm_list_items = [f'{l[1]} listener - name: {l[0]}' for l in listeners]
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
            accept_keys=('enter', 'ctrl-e', 'ctrl-w'),
            preview_command=self.listener_preview,
            preview_size=0.85,
            preview_title=f'{Style.BRIGHT}Listener Details{Style.RESET_ALL}'
        )

        ### Listener Kill Menu
        ### use same items fo prev menu
        lm_kill_title = '\n\n       Listeners Killer\n'
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

        lmm_sel = lmm.show()

        if lmm.chosen_accept_key == 'ctrl-w':
            self.on_activate_l()
        elif lmm.chosen_accept_key == 'ctrl-e':
            self.on_activate_r()
        else:
            if lmm_sel == 0:
                ## Listeners list menu "Show Listeners"
                while not lm_list_back:
                    lm_list_sel = lm_list_menu.show()

                    if lm_list_menu.chosen_accept_key == 'ctrl-w':
                        lm_list_back = True
                        self.on_activate_l()
                    elif lm_list_menu.chosen_accept_key == 'ctrl-e':
                        lm_list_back = True
                        self.on_activate_r()
                    else:
                        # if lm_list_items[lm_list_sel] not in ['NO ACTIVE LISTENERS', 'Back']:
                        listener_string = lm_list_items[lm_list_sel]
                        if listener_string not in ['NO ACTIVE LISTENERS', 'Back']:
                            ## Payload creator menu
                            payload_menu_title = '\n\n       Choose the payload type\n'
                            # get payloads for specific listener
                            payload_types_array = self.payloads_types[listener_string.split()[0]]
                            if payload_types_array[-1] != 'Back':
                                payload_types_array.append('Back')
                            payload_menu = TerminalMenu(
                                menu_entries=payload_types_array,
                                title=payload_menu_title,
                                menu_cursor=self.cursor,
                                menu_cursor_style=self.cursor_style,
                                menu_highlight_style=self.h_style,
                                cycle_cursor=True,
                                clear_screen=False,
                                accept_keys=('enter', 'ctrl-e', 'ctrl-w')
                                # preview_command=self.listener_preview,
                                # preview_size=0.85,
                                # preview_title=f'{Style.BRIGHT}Listener Details{Style.RESET_ALL}'
                            )

                            payload_menu_sel = payload_menu.show()
                            if payload_menu.chosen_accept_key == 'ctrl-w':
                                lm_list_back = True
                                self.on_activate_l()
                            elif payload_menu.chosen_accept_key == 'ctrl-e':
                                lm_list_back = True
                                self.on_activate_r()
                            else:
                                if payload_types_array[payload_menu_sel] != 'Back':
                                    self.create_payload(listener_string.split()[-1], payload_types_array[payload_menu_sel])
                                    lm_list_back = True
                        else:
                            lm_list_back = True

            elif lmm_sel == 1:
                ## start listener menu "New Listener"
                self.start_listener()
            
            elif lmm_sel == 2:
                ## kill listener menu "Kill Listener"
                lm_kill_sel = lm_kill_menu.show()

                if lm_kill_menu.chosen_accept_key == 'ctrl-w':
                    self.on_activate_l()
                elif lm_kill_menu.chosen_accept_key == 'ctrl-e':
                    self.on_activate_r()
                else:
                    if lm_list_items[lm_kill_sel] not in ['NO ACTIVE LISTENERS', 'Back']:
                        listener_tokill = lm_list_items[lm_kill_sel].split()[-1]
                        type_tokill = lm_list_items[lm_kill_sel].split()[0]
                        self.stash.sql_stash( 'UPDATE key_store SET alive = ? WHERE list_name = ? ;', (False, listener_tokill) )
                        self.kill_listener(type_tokill,listener_tokill)

    def start_listener(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.listener_completer)
        already_running = 1
        while already_running:
            header = f'\n\n       Start a new listener, Tab is your friend. "back" to go back. <Listener Type> <Args>. Which args? Just input the listener type.'
            cmd = input(f'{header}\n{Fore.GREEN}{Style.BRIGHT}{self.cursor}{Style.RESET_ALL}')

            if cmd == '':
                continue

            exp_cmd = cmd.split()
            if exp_cmd[0] == 'back':
                already_running = 0
                continue

            elif exp_cmd[0] in ['HTTPS','HTTP']:
                if len(exp_cmd) != 4:
                    error(f'<HTTPS|HTTP> <listener name> <IP> <PORT>')
                    already_running = 0
                    continue
                else:
                    http_type,l_name,ip,port = exp_cmd

                    if ' ' in l_name:
                        error(f'No spaces!')
                        already_running = 0
                        continue

                    try:
                        ip_address(ip)
                    except:
                        error(f'Not an IP address')
                        already_running = 0
                        continue

                    if '0.0.0.0' == ip:
                        error('Use the specific IP of one of your ifaces')
                        already_running = 0
                        continue

                    try:
                        if 0 < int(port) < 65536:
                            pass
                        else:
                            raise Exception('WTF')
                    except:
                        error(f'WTF is that port??')
                        already_running = 0
                        continue

                    if l_name in self.listeners.keys():
                        error(f'Listener with that name already exist.')
                        already_running = 0
                        continue
                    elif self.stash.check_ip_n_port(ip, int(port)):
                        error(f'Port Already in use for that iface.')
                        already_running = 0
                        continue
                    else:
                        self.listeners[l_name] = HTTP_listener(http_type, l_name, ip, int(port), self.stash, self.debug)

            already_running = 0
            self.listeners[l_name].start()


    def kill_listener(self, l_type, l_name):
        if l_type in ['HTTPS','HTTP']:
            self.listeners[l_name].stop()

    def create_payload(self, name, ptype):
        listener_info = self.stash.get_listener(name)
        l_type = listener_info[0][0]
        l_ip = listener_info[0][1]
        l_port = listener_info[0][2]
        l_key = self.stash.get_key(name)[0][0]
        cwd = getcwd()
        template_folder = path.join(cwd, 'beacons')
        out_folder = path.join(cwd, 'payloads')
        if l_type in ['HTTPS','HTTP']:
            if ptype == 'powershell':
                template = path.join(template_folder,'https_beacon.ps1')
                with open(template,'r') as tr:
                    temp = tr.read()
                temp = temp.replace('XXX_listener_ip_placeholder_XXX',l_ip)
                temp = temp.replace('XXX_listener_port_placeholder_XXX',str(l_port))
                temp = temp.replace('XXX_listener_key_placeholder_XXX',l_key)
                if l_type == 'HTTPS':
                    temp = temp.replace('http','https')
                final_implant = path.join(out_folder,f'{l_type}_beacon_{"".join(x for x in name if x.isalnum())}_{"".join(choice(ascii_letters) for i in range(5))}.ps1')
                with open(final_implant,'w+') as fw:
                    fw.write(temp)
                success(f'The payload is ready --> {final_implant}')