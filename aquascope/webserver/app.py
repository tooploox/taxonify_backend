import os
import logging

from flask import Flask, request
from flask_restful import Api
from pymongo import MongoClient

import aquascope.webserver.api as api

mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
mongo_client = MongoClient(mongo_connection_string)
db = mongo_client.get_database()

logging.basicConfig(filename='webserver.log', level=logging.DEBUG,
                    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
app = Flask(__name__)
app.config['db'] = db


@app.after_request
def after_request(response):
    app.logger.error('%s %s %s %s %s',  request.remote_addr, request.method,
                     request.scheme, request.full_path, response.status)
    return response


server_api = Api(app)
server_api.add_resource(api.DummyEndpoint, '/')
server_api.add_resource(api.DummyTaskEndpoint, '/task')


if __name__ == "__main__":
    app.run()
