# coding: utf-8

import pytest
import datetime as dt
import json

from flask import url_for
from facelo.exceptions import USER_ALREADY_REGISTERED
from .factories import UserFactory

def _register_user(client, **kwargs):
    return client.post(url_for("user.register_user"), json={
        "email": "mo@mo.mo",
        "password": "momo"
    }, **kwargs)

# def _register_user(client, **kwargs):
#     user_json = {
#         "email": "mo@mo.mo",
#         "password": "momo"
#     }
#     print(user_json)
#     print(type(user_json))

# def _register_user(client, **kwargs):
#     user_dict = UserFactory.stub().__dict__
#     return client.post(url_for("user.register_user"), json=user_dict, **kwargs)


@pytest.mark.usefixtures('db')
class TestAuthenticate:

    def test_register_user(self, client):
        resp = _register_user(client)
        assert resp.json['email'] == 'mo@mo.mo'
        assert resp.json['token'] != 'None'
        assert resp.json['token'] != ''

    def test_user_login(self, client):
        _register_user(client)

        resp = client.post(url_for('user.login_user'), json={
            'email': 'mo@mo.mo',
            'password': 'momo'
        })

        assert resp.json['email'] == 'mo@mo.mo'
        assert resp.json['token'] != 'None'
        assert resp.json['token'] != ''

    def test_get_user(self, client):
        resp = _register_user(client)
        token = str(resp.json['token'])
        resp = client.get(url_for('user.get_user'), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert resp.json['email'] == 'mo@mo.mo'

    def test_register_already_registered_user(self, client):
        _register_user(client)
        resp = _register_user(client)
        assert resp.status_code == 422
        assert resp.json == USER_ALREADY_REGISTERED['message']

    def test_update_user(self, client):
        resp = _register_user(client)
        token = str(resp.json['token'])
        resp = client.put(url_for('user.update_user'), json={
                'email': 'meh@mo.mo',
                'password': 'hmm'
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert resp.json['email'] == 'meh@mo.mo'
