import os
import logging

from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_restful import Api
from pymongo import MongoClient

import aquascope.webserver.api as api
from aquascope.webserver.data_access.storage.blob import blob_storage_client

mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
mongo_client = MongoClient(mongo_connection_string)
db = mongo_client.get_database()

logging.basicConfig(filename='webserver.log', level=logging.DEBUG,
                    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
app = Flask(__name__)
app.config['db'] = db
app.config['storage_client'] = blob_storage_client(connection_string=os.environ['STORAGE_CONNECTION_STRING'])

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['AQUASCOPE_TEST_USER'] = os.environ['AQUASCOPE_TEST_USER']
app.config['AQUASCOPE_TEST_PASS'] = os.environ['AQUASCOPE_TEST_PASS']
app.config['ENVIRONMENT'] = os.environ['ENVIRONMENT']

if app.config['ENVIRONMENT'] != 'production':
    # We need CORS only for Swagger so it's safer to not have it in production
    from flask_cors import CORS

    CORS(app)

jwt = JWTManager(app)


@app.after_request
def after_request(response):
    app.logger.error('%s %s %s %s %s', request.remote_addr, request.method,
                     request.scheme, request.full_path, response.status)
    return response


server_api = Api(app)
server_api.add_resource(api.DummyEndpoint, '/')
server_api.add_resource(api.DummyTaskEndpoint, '/task')
server_api.add_resource(api.UserLogin, '/user/login')
server_api.add_resource(api.UserTokenRefresh, '/user/refresh')
server_api.add_resource(api.Items, '/items')
server_api.add_resource(api.Sas, '/sas')


if __name__ == "__main__":
    app.run()
