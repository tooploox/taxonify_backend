import unittest

from flask import json

from aquascope.tests.aquascope.webserver.data_access.db.dummy_users import DUMMY_USERS, \
    DUMMY_USERS_WITH_DEFAULT_PROJECTION
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

    def test_api_can_post_login_with_user_from_db(self):
        request_data = json.dumps({
            'username': DUMMY_USERS[0]['username'],
            'password': self.auth_pass_raw
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_api_cant_post_login_with_wrong_password(self):
        request_data = json.dumps({
            'username': self.auth_user,
            'password': self.auth_pass_raw + 'dummy'
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 401)

    def test_api_cant_post_login_with_wrong_username(self):
        request_data = json.dumps({
            'username': self.auth_user + 'dummy',
            'password': self.auth_pass_raw
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 401)

    def test_api_cant_post_login_with_missing_argument(self):
        request_data = json.dumps({
            'username': self.auth_user
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_api_cant_post_login_with_bad_argument(self):
        request_data = json.dumps({
            'username': self.auth_user,
            'password': self.auth_pass_raw,
            'dummy': 'value'
        })

        res = self.client().post('/user/login', data=request_data,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 400)


class TestUserList(FlaskAppTestCase):
    def test_api_can_get_user_list(self):
        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION
        self.assertCountEqual(response, expected_users)


class TestUserNew(FlaskAppTestCase):
    def test_api_can_post_new_user(self):
        new_user = dict(username='newuser')
        request_data = json.dumps(new_user)

        res = self.client().post('/user/new', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION + [new_user]
        self.assertCountEqual(response, expected_users)

    def test_api_cant_post_new_user_with_already_existing_username(self):
        new_user = dict(username=DUMMY_USERS[0]['username'])
        request_data = json.dumps(new_user)

        res = self.client().post('/user/new', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION
        self.assertCountEqual(response, expected_users)

    def test_api_cat_post_new_user_with_already_existing_username_but_different_case(self):
        new_user = dict(username=DUMMY_USERS[0]['username'].capitalize())
        request_data = json.dumps(new_user)

        res = self.client().post('/user/new', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION + [new_user]
        self.assertCountEqual(response, expected_users)

    def test_api_cant_post_new_user_with_forbidden_characters(self):
        new_user = dict(username='us#r$')
        request_data = json.dumps(new_user)

        res = self.client().post('/user/new', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION
        self.assertCountEqual(response, expected_users)

    def test_api_cant_post_new_user_with_username_too_short(self):
        new_user = dict(username='')
        request_data = json.dumps(new_user)

        res = self.client().post('/user/new', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION
        self.assertCountEqual(response, expected_users)

    def test_api_cant_post_new_user_with_username_too_long(self):
        new_user = dict(username='u' * 65)
        request_data = json.dumps(new_user)

        res = self.client().post('/user/new', data=request_data, headers=self.headers)
        self.assertEqual(res.status_code, 400)

        res = self.client().get('/user/list', headers=self.headers)
        self.assertEqual(res.status_code, 200)

        response = res.json
        expected_users = DUMMY_USERS_WITH_DEFAULT_PROJECTION
        self.assertCountEqual(response, expected_users)


if __name__ == '__main__':
    unittest.main()
