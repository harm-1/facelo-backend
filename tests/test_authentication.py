# coding: utf-8

import pytest
import json

from flask import url_for
from facelo.exceptions import USER_ALREADY_REGISTERED, USER_NOT_FOUND, USER_PASSWORD_INCORRECT

from .factories import UserFactory

@pytest.fixture
def user_dict(kwargs):
    return UserFactory.stub(**kwargs).__dict__

@pytest.fixture
def register_user(client, user_dict):
    user_dict['birth_day'] = str(user_dict['birth_day'])
    return client.post(url_for("user.register_user"), json=user_dict)

@pytest.mark.usefixtures('db')
class TestAuthenticate:

    def test_register_user(self, user_dict, register_user):
        assert register_user.json['email'] == user_dict['email']
        assert register_user.json['token'] != 'None'
        assert register_user.json['token'] != ''

    def test_register_already_registered_user(self, client, user_dict, register_user):
        resp = client.post(url_for("user.register_user"), json=user_dict)
        assert resp.status_code == 422
        assert resp.json == USER_ALREADY_REGISTERED['message']

    def test_user_login(self, client, user_dict, register_user):
        resp = client.post(url_for('user.login_user'), json=user_dict)
        assert resp.json['email'] == user_dict['email']
        assert resp.json['token'] != 'None'
        assert resp.json['token'] != ''

    @pytest.mark.kwargs(email='foo@bar.com', password='foobar')
    @pytest.mark.parametrize("credentials,status_code", [
        ({'email': 'foo@bar.com', 'password': 'foobar'}, 200),
        ({'email': 'bar@foo.com', 'password': 'foobar'}, 404),
        ({'email': 'foo@bar.com', 'password': 'barfoo'}, 401),])
    def test_login_response_codes(self, client, register_user, credentials, status_code):
        resp = client.post(url_for('user.login_user'), json=credentials)
        assert resp.status_code == status_code

    def test_get_user(self, client, user_dict, register_user):
        token = str(register_user.json['token'])
        resp = client.get(url_for('user.get_user'), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert resp.json['email'] == user_dict['email']

    def test_update_user(self, client, user_dict, register_user):
        token = str(register_user.json['token'])
        resp = client.put(url_for('user.update_user'), json=user_dict, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert resp.json['email'] == user_dict['email']

    def test_bad_authorization(self, client, user_dict, register_user):
        resp = client.get(url_for('user.get_user'), headers={
            'Authorization': ''
        })
        assert resp.status_code == 401
