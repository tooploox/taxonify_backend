import datetime

from flask import current_app as app
from flask_restful import Resource

from aquascope.tasks.celery import celery_app


class DummyEndpoint(Resource):
    def get(self):
        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}

        db = app.config['db']
        id = db.posts.insert_one(post).inserted_id
        return f'Hello world {id}'


class DummyTaskEndpoint(Resource):
    def get(self):
        app.logger.debug('somebody wants me to run a task')

        celery_app.send_task('aquascope.tasks.add.task',
                             args=[5, 3])
        return "I'm about to schedule a task."
