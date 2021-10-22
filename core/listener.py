from flask import Flask, render_template
from multiprocessing import Process

class HTTP_listener:

	def __init__(self, name, ip, port):
		self.name = name
		self.ip = ip
		self.port = port

		self.app = Flask(__name__)
		self.html_fold = 'html/'

		@app.errorhandler(404)
		def page_not_found(error):
			return render_template('404.html', title = '404'), 404

		@self.app.route('/', methods=['GET'])
		def index():
			return "Hello there!"