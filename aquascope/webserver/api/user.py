from passlib.hash import pbkdf2_sha256 as sha256

from flask import current_app as app
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity)


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        args = parser.parse_args(strict=True)

        try:
            verified_user = sha256.verify(args['password'],
                                          app.config['AQUASCOPE_TEST_PASS'])
        except ValueError as e:
            app.logger.error(e)
            return {'message': 'Server error'}, 500
        else:
            if verified_user and args['username'] == app.config['AQUASCOPE_TEST_USER']:
                access_token = create_access_token(identity=args['username'])
                refresh_token = create_refresh_token(identity=args['username'])
                return {
                    'message': 'Logged in as {}'.format(args['username']),
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
