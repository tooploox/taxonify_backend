import datetime
import os
import logging

from flask import Flask, request
from pymongo import MongoClient

from aquascope.tasks.celery import celery_app

mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
mongo_client = MongoClient(mongo_connection_string)
db = mongo_client.get_database()

logging.basicConfig(filename='webserver.log', level=logging.DEBUG,
                    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
app = Flask(__name__)


@app.after_request
def after_request(response):
    app.logger.error('%s %s %s %s %s',  request.remote_addr, request.method,
                     request.scheme, request.full_path, response.status)
    return response


@app.route('/')
def mainpoint():
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    id = db.posts.insert_one(post).inserted_id
    return f'Hello world {id}'


@app.route('/task')
def task():
    app.logger.debug('somebody wants me to run a task')

    celery_app.send_task('aquascope.tasks.add.task',
                         args=[5, 3])
    return "I'm about to schedule a task."


if __name__ == "__main__":
    app.run()
