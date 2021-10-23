import sys
import threading

from flask import Flask, render_template
from multiprocessing import Process

aa = 'banane'

def ciao(a):
	print( aa )

name = "test"
ip = "127.0.0.1"
port = 9090

html_fold = '/home/blu/Documents/projectz/wtf_another_c2/core/html/'
app = Flask(__name__, template_folder=html_fold)
running = True

@app.route('/', methods=['GET'])
def index():
    return "Hello there!", 200

@app.route('/lol', methods=['GET'])
def lol():
    return "Hollo thoro!", 200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title = '404'), 404

print('aaa')
def run(port, ip):
	app.logger.disabled = False
	app.run(port=port, host=ip, debug=True)

print('aaa')
server = Process(target=run, args=(port,ip,))

## no server banner
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

print('aaa')
daemon = threading.Thread(name = name, target = server.start, args = (), daemon = True)
# daemon.daemon = True
daemon.start()

running = True

print('aaa')
input()

server.terminate()
server = None
daemon = None
running = False