import sys
import threading

from flask import Flask, render_template, request
from multiprocessing import Process

class HTTP_listener:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

        ## to fix
        html_fold = '/home/blu/Documents/projectz/wtf_another_c2/core/html/'
        self.app = Flask(__name__, template_folder=html_fold)

        self.running = True

        @self.app.route('/', methods=['GET'])
        def index():
            return 'Hello there!'

        @self.app.route('/test', methods=['GET'])
        def test():
            return 'Test there!'
        
        @self.app.errorhandler(404)
        def page_not_found(error):
            return render_template(f'404.html', title = '404'), 404

    def run(self):
        # to fix (debug False and logger True)
        self.app.logger.disabled = True
        self.app.run(port=self.port, host=self.ip, debug=False)

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