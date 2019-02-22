from passlib.hash import pbkdf2_sha256 as sha256

from flask import current_app as app, request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity,
                                jwt_required)
from pymongo.errors import DuplicateKeyError

from aquascope.webserver.data_access.db import users
from aquascope.webserver.schema.user import UserSchema, NewUserSchema
from aquascope.webserver.schema.custom_schema import FormattedValidationError


class UserLogin(Resource):
    def post(self):
        schema = UserSchema()
        try:
            args = schema.load(request.get_json())
        except FormattedValidationError as e:
            return e.formatted_messages, 400

        db = app.config['db']
        username, password = args['username'], args['password']

        try:
            verified_password = sha256.verify(password,
                                          app.config['AQUASCOPE_TEST_PASS'])
        except ValueError as e:
            app.logger.error(e)
            return {'message': 'Server error'}, 500
        else:
            verified_user = username == app.config['AQUASCOPE_TEST_USER'] or users.exists(db, username)

            if verified_password and verified_user:
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                return {
                    'message': 'Logged in as {}'.format(username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            else:
                return {'message': 'Wrong credentials'}, 401


class UserTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class UserList(Resource):
    @jwt_required
    def get(self):
        db = app.config['db']
        docs = users.list_all(db)
        return list(docs)


class UserNew(Resource):
    @jwt_required
    def post(self):
        pass
        json_data = request.get_json(force=True)
        schema = NewUserSchema()

        try:
            args = schema.load(json_data)
        except FormattedValidationError as e:
            return e.formatted_messages, 400

        db = app.config['db']

        try:
            users.create(db, args['username'])
        except DuplicateKeyError:
            return dict(message='User already exists in the system.'), 401

        return None, 204
