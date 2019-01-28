import unittest

from flask import json

from aquascope.tests.flask_app_test_case import FlaskAppTestCase


class TestUserLogin(FlaskAppTestCase):

    def test_api_can_post_login_with_proper_credentials(self):
        request_data = json.dumps({
            'username': self.auth_user,
            'password': self.auth_pass_raw
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_api_can_post_login_with_wrong_password(self):
        request_data = json.dumps({
            'username': self.auth_user,
            'password': self.auth_pass_raw + 'dummy'
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 401)

    def test_api_can_post_login_with_wrong_username(self):
        request_data = json.dumps({
            'username': self.auth_user + 'dummy',
            'password': self.auth_pass_raw
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 401)

    def test_api_can_post_login_with_missing_argument(self):
        request_data = json.dumps({
            'username': self.auth_user
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_api_can_post_login_with_bad_argument(self):
        request_data = json.dumps({
            'username': self.auth_user,
            'password': self.auth_pass_raw,
            'dummy': 'value'
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
