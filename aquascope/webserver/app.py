import logging
import os

from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_restful import Api

from aquascope.tasks.celery import make_celery_app
import aquascope.webserver.api as api
from aquascope.webserver.data_access.db.util import get_db_from_env
from aquascope.webserver.data_access.storage.blob import blob_storage_client


def make_app(db, storage_connection_string, jwt_secret_key,
             aquascope_test_user, aquascope_test_pass, aquascope_secondary_pass,
             environment, celery_user, celery_password, celery_address, page_size):
    logging.basicConfig(filename='webserver.log', level=logging.DEBUG,
                        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    logging.getLogger("azure.storage").setLevel(logging.CRITICAL)

    app = Flask(__name__)
    app.config['db'] = db
    app.config['storage_client'] = blob_storage_client(connection_string=storage_connection_string)
    app.config['celery'] = make_celery_app(celery_user, celery_password, celery_address)
    app.config['page_size'] = page_size
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = jwt_secret_key
    app.config['AQUASCOPE_TEST_USER'] = aquascope_test_user
    app.config['AQUASCOPE_TEST_PASS'] = aquascope_test_pass
    app.config['AQUASCOPE_SECONDARY_PASS'] = aquascope_secondary_pass
    app.config['ENVIRONMENT'] = environment

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
    server_api.add_resource(api.UserList, '/user/list')
    server_api.add_resource(api.UserNew, '/user/new')
    server_api.add_resource(api.Items, '/items')
    server_api.add_resource(api.PagedItems, '/items/paged')
    server_api.add_resource(api.Sas, '/sas')
    server_api.add_resource(api.UploadTags, '/upload/<string:upload_id>/tags')
    server_api.add_resource(api.UploadPut, '/upload/<string:filename>')
    server_api.add_resource(api.UploadGet, '/upload/<string:upload_id>')
    server_api.add_resource(api.UploadList, '/upload/list')
    server_api.add_resource(api.Export, '/export')

    return app


def get_app():
    storage_connection_string = os.environ['STORAGE_CONNECTION_STRING']
    jwt_secret_key = os.environ['JWT_SECRET_KEY']
    aquascope_test_user = os.environ['AQUASCOPE_TEST_USER']
    aquascope_test_pass = os.environ['AQUASCOPE_TEST_PASS']
    aquascope_secondary_pass = os.environ['AQUASCOPE_SECONDARY_PASS']
    environment = os.environ['ENVIRONMENT']
    celery_user = os.environ['CELERY_USER']
    celery_password = os.environ['CELERY_PASS']
    celery_address = os.environ['CELERY_ADDRESS']
    page_size = os.environ['PAGE_SIZE'] if 'PAGE_SIZE' in os.environ else 500

    db = get_db_from_env()
    app = make_app(db, storage_connection_string, jwt_secret_key,
                   aquascope_test_user, aquascope_test_pass, aquascope_secondary_pass,
                   environment, celery_user, celery_password, celery_address, page_size)
    return app


if __name__ == "__main__":
    app = get_app()
    app.run()
