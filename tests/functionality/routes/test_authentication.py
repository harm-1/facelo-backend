# CODING: utf-8

import json

import pytest
from flask import url_for

from facelo.exceptions import (USER_ALREADY_REGISTERED, USER_NOT_FOUND,
                               USER_PASSWORD_INCORRECT)
from facelo.user.serializers import LoginSchema, UserSchema
from factories import UserFactory


@pytest.fixture
def register_dict(user_dict):
    result = dict(user_dict)
    result.pop('karma')
    result["birth_day"] = str(user_dict["birth_day"])

    # My terms and condition is currently probably not what it should be
    assert 'terms_accepted' not in user_dict
    result['terms_accepted'] = "True"

    return result


@pytest.fixture
def login_dict(user_dict):
    result = dict(user_dict)
    for k in ['karma', 'birth_day', 'gender', 'sexual_preference']:
        result.pop(k)
    return result


@pytest.fixture
def register_user(client, register_dict):
    return client.post(url_for("user.register_user"), json=register_dict)


@pytest.mark.usefixtures("db")
class TestAuthenticate:

    def test_serializer(self, client):
        response = client.post(url_for("user.register_user"), json={})
        assert response.status_code == 422

    def test_register_user(self, user_dict, register_user):
        assert register_user.json["email"] == user_dict["email"]
        assert register_user.json["token"] != "None"
        assert register_user.json["token"] != ""

    def test_register_already_registered_user(self, client, register_dict, register_user):
        resp = client.post(url_for("user.register_user"), json=register_dict)
        assert resp.status_code == 422
        assert resp.json == USER_ALREADY_REGISTERED["message"]

    def test_user_login(self, client, login_dict, register_user):
        resp = client.post(url_for("user.login_user"), json=login_dict)
        assert resp.json["email"] == login_dict["email"]
        assert resp.json["token"] != "None"
        assert resp.json["token"] != ""

    # yapf: disable
    @pytest.mark.parametrize("user_dict",
        [{"email": "foo@bar.com", "password": "foobar"}], indirect=True)
    @pytest.mark.parametrize("credentials, code",
        [({"email": "foo@bar.com", "password": "foobar"}, 200),
         ({"email": "bar@foo.com", "password": "foobar"}, 404),
         ({"email": "foo@bar.com","password": "barfoo"}, 401)])
    def test_login_response_codes(self, client, register_user, credentials, code):
        resp = client.post(url_for("user.login_user"), json=credentials)
        assert resp.status_code == code
    # yapf: enable

    def test_get_user(self, client, user_dict, register_user):
        token = str(register_user.json["token"])
        resp = client.get(url_for("user.get_user"), headers={"Authorization": "Bearer {}".format(token)})
        assert resp.json["email"] == user_dict["email"]

    def test_update_user(self, client, register_dict, register_user):
        token = str(register_user.json["token"])
        resp = client.put(url_for("user.update_user"),
                          json=register_dict,
                          headers={"Authorization": "Bearer {}".format(token)})
        assert resp.json["email"] == register_dict["email"]

    def test_bad_authorization(self, client, user_dict, register_user):
        resp = client.get(url_for("user.get_user"), headers={"Authorization": ""})
        assert resp.status_code == 401
