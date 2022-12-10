from core.stash import *
from colorama import Fore, Back, Style
from pynput.keyboard import Key, Listener
from os import get_terminal_size, system, name

class LessPy :
    def __init__(self, agent_name, stash):
        # Beacon Name - Listener - Remote IP - Hostname - Beacon Type
        self.stash = stash
        
        # self.a_name,self.l_name,self.ip,self.h_name,self.t_beacon,self.alive,self.time_stamp = info_string.split(' - ')
        agent_info = self.stash.get_agents(full=True,agent=agent_name)[0]
        self.a_name,self.l_name,self.ip,self.h_name,self.t_beacon,self.alive,self.time_stamp = agent_info
        
        self.columns, self.rows = get_terminal_size()
        self.rows -= 1
        self.full_list = self.gen_list(self.a_name, self.l_name)
        self.index = 0

    def clear_screen(self):
        system('cls' if name == 'nt' else 'clear')

    def lessPy(self):
        self.clear_screen()
        # print(self.full_list)
        # input()
        # print(len(self.full_list))
        # exit()
        # print(self.index)
        # print(self.rows)
        # for i in range(0,51):
        #     print(self.full_list[i])
        # exit()

        if self.rows < len(self.full_list):
            for i in range(self.index,self.rows):
                print(self.full_list[i])
            with Listener( on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        else:
            for i in self.full_list:
                print(i)
            with Listener( on_release=self.on_release) as listener:
                listener.join()

    def on_press(self,key):
        k = str(key).replace("'", "")
        if k == 'w' or key == Key.up:
            self.index -= 1 if self.index > 0 else 0
        elif k == 's' or key == Key.down:
            self.index += 1 if self.index < (len(self.full_list)-self.rows) else 0
        elif key == Key.page_down:
            if self.index < (len(self.full_list)-(self.rows*2)):
                self.index += self.rows
            else:
                self.index = len(self.full_list)-self.rows
        elif key == Key.page_up:
            if self.index > (self.rows):
                self.index -= self.rows
            else:
                self.index = 0
        elif key == Key.home:
            self.index = 0
        elif key == Key.end:
            self.index = len(self.full_list)-self.rows
        # elif k == '/':
        #     print('\t/', end='')

        self.clear_screen()
        for i in range(self.index,(self.index+self.rows)):
            print(self.full_list[i])

    def on_release(self,key):
        if key == Key.esc or str(key).replace("'", "") == 'q':
            return False
   

    def gen_list(self, agent, listener):
        header = f'{"-"*(int(self.columns/2)-10)}Beginning of History{"-"*(int(self.columns/2)-10)}'
        ret = [header[index : index + self.columns] for index in range(0,len(header), self.columns)]
        ret.append(' ')
        intro = f'{Style.BRIGHT}Full command list fort aget {Fore.GREEN}{agent}{Fore.WHITE} connected to {Fore.GREEN}{listener}{Fore.WHITE}'
        c_intro = [intro[index : index + self.columns] for index in range(0,len(intro), self.columns)]
        ret += c_intro
        ret.append(f'First seen: {Fore.GREEN}{self.time_stamp}{Fore.WHITE}')
        if self.alive:
            general_data = f'Current status: {Fore.GREEN}Alive{Fore.WHITE}'
        else:
            general_data = f'Current status: {Fore.RED}Dead{Fore.WHITE}'
        c_general_data = [general_data[index : index + self.columns] for index in range(0,len(general_data), self.columns)]
        ret += c_general_data
        ret.append(f'Agent IP: {Fore.GREEN}{self.ip}{Fore.WHITE}')
        ret.append(f'Agent Hostname: {Fore.GREEN}{self.h_name}{Fore.WHITE}')
        ret.append(f'Agent Type: {Fore.GREEN}{self.t_beacon}{Fore.WHITE}')
        ret.append(' ')
        high_comm = f'{Fore.GREEN}{Style.BRIGHT}Task - {Fore.WHITE}'
        high_resp = f'{Fore.CYAN}Result > '
        comms = self.stash.get_agents_comm_list(agent)
        ret += [' ']
        for c in comms:
            cra = c[1].replace('\r','').split('\n')
            cr = cra[0]
            command = f'{high_comm}{c[2]} {Fore.GREEN}>{Fore.WHITE} {c[0]}'
            c_command = [command[index : index + self.columns] for index in range(0,len(command), self.columns)]
            ret += c_command
            if len(cra) > 1:
                response = f'{high_resp}{cr.rstrip()}'
                c_response = [response[index : index + self.columns] for index in range(0,len(response), self.columns)]
                ret += c_response
                for i in range(1,len(cra)):
                    if i != '' :
                        extra = f'{Fore.CYAN}{cra[i].rstrip()}{Style.RESET_ALL}'
                        c_extra = [extra[index : index + self.columns] for index in range(0,len(extra), self.columns)]
                        ret += c_extra
            else:
                noresp = f'{high_resp}{Fore.RED}No response yet :({Style.RESET_ALL}'
                c_noresp = [noresp[index : index + self.columns] for index in range(0,len(noresp), self.columns)]
                ret += c_noresp

        footer = f'{"-"*(int(self.columns/2)-7)}End of History{"-"*(int(self.columns/2)-7)}'
        c_footer = [footer[index : index + self.columns] for index in range(0,len(footer), self.columns)]
        ret += c_footer
        # for r in ret:
        #     with open('/tmp/ccc','a+') as fw:
        #         fw.write(f'{r}\n')
        # exit()
        return ret

