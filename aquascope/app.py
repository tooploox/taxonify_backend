from flask import Flask, request
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
app = Flask(__name__)


@app.after_request
def after_request(response):
    app.logger.error('%s %s %s %s %s',  request.remote_addr, request.method,
                     request.scheme, request.full_path, response.status)
    return response


@app.route('/')
def mainpoint():
    return "Hello world."


@app.route('/task')
def task():
    app.logger.debug('somebody wants me to run a task')
    return "I'm about to schedule a task."
