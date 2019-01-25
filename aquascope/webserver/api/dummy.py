import datetime

from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource


class DummyEndpoint(Resource):
    @jwt_required
    def get(self):
        user = get_jwt_identity()
        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}

        db = app.config['db']
        id = db.posts.insert_one(post).inserted_id
        return f'Hello {user} {id}'


class DummyTaskEndpoint(Resource):
    @jwt_required
    def get(self):
        app.logger.debug('somebody wants me to run a task')

        celery_app = app.config['celery']
        celery_app.send_task('aquascope.tasks.add.task',
                             args=[5, 3])
        return "I'm about to schedule a task."
