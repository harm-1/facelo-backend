# coding: utf-8

import pytest
import datetime as dt
import json

from flask import url_for
from facelo.exceptions import USER_ALREADY_REGISTERED, USER_NOT_FOUND, USER_PASSWORD_INCORRECT
from .factories import UserFactory

@pytest.fixture
def user_dict():
    user_dict = UserFactory.stub().__dict__
    user_dict['birth_day'] = str(user_dict['birth_day'])
    return user_dict

@pytest.fixture
def register_user(client, user_dict, kwargs):
    return client.post(url_for("user.register_user"), json=user_dict, **kwargs)


@pytest.mark.usefixtures('db')
class TestAuthenticate:

    def test_register_user(self, user_dict, register_user):
        assert register_user.json['email'] == user_dict['email']
        assert register_user.json['token'] != 'None'
        assert register_user.json['token'] != ''

    def test_user_login(self, client, user_dict, register_user):
        resp = client.post(url_for('user.login_user'), json=user_dict)

        assert resp.json['email'] == user_dict['email']
        assert resp.json['token'] != 'None'
        assert resp.json['token'] != ''

    def test_user_login_wrong_email(self, client, register_user):
        resp = client.post(url_for('user.login_user'), json={
            'email': 'incorrect@stuff.com',
            'password': 'incorrect'
        })

        assert resp.status_code == 404
        assert resp.json == USER_NOT_FOUND['message']

    def test_user_login_wrong_password(self, client, user_dict, register_user):
        resp = client.post(url_for('user.login_user'), json={
            'email': user_dict['email'],
            'password': 'incorrect'
        })

        assert resp.status_code == 401
        assert resp.json == USER_PASSWORD_INCORRECT['message']

    def test_get_user(self, client, user_dict, register_user):
        token = str(register_user.json['token'])
        resp = client.get(url_for('user.get_user'), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert resp.json['email'] == user_dict['email']

    def test_register_already_registered_user(self, client, user_dict, register_user):
        resp = client.post(url_for("user.register_user"), json=user_dict)

        assert resp.status_code == 422
        assert resp.json == USER_ALREADY_REGISTERED['message']

    def test_update_user(self, client, user_dict, register_user):
        token = str(register_user.json['token'])
        resp = client.put(url_for('user.update_user'), json=user_dict, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert resp.json['email'] == user_dict['email']
