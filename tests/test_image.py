# coding: utf-8

import pytest
import datetime as dt
import json

from flask import url_for
from .factories import UserFactory, ImageFactory

@pytest.fixture
def user_dict(kwargs):
    user_dict = UserFactory.stub(**kwargs).__dict__
    user_dict['birth_day'] = str(user_dict['birth_day'])
    return user_dict

@pytest.fixture
def register_user(client, user_dict):
    return client.post(url_for("user.register_user"), json=user_dict)

@pytest.fixture
def user(client, db):
    user_dict = UserFactory.stub().__dict__
    user = UserFactory(**user_dict).save()
    resp = client.post(url_for('user.login_user'),
                       json={'email': user_dict['email'], 'password':user_dict['password']})
    yield user
    user.delete()

@pytest.fixture
def image_dict():
    image_dict = ImageFactory.stub().__dict__
    image_dict['created'] = str(image_dict['created'])
    image_dict['uploaded'] = str(image_dict['uploaded'])
    del image_dict['user']
    return image_dict

@pytest.fixture
def upload_image(client, image_dict, register_user):
    token = str(register_user.json['token'])
    resp = client.post(url_for("image.upload_image"), json=image_dict, headers={
        'Authorization': 'Bearer {}'.format(token)})
    return resp

@pytest.fixture
def image(db, user):
    image = ImageFactory(user=user).save()
    yield image
    image.delete()


@pytest.mark.usefixtures('db')
class TestImage:

    def test_get_images(self, client, register_user, image_dict, upload_image):
        token = str(register_user.json['token'])
        resp = client.get(url_for('image.get_images'), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert(isinstance(resp.json, list))

    def test_get_image(self, client, user, image):
        resp = client.get(url_for('image.get_image', image_id=image.id),
                          headers={'Authorization': 'Bearer {}'.format(user.token)})
        assert resp.json['image_url'] == image.__dict__['image_url']

    def test_post_image(self, client, register_user, image_dict):
        token = str(register_user.json['token'])
        resp = client.post(url_for("image.upload_image"), json=image_dict, headers={
            'Authorization': 'Bearer {}'.format(token)})
        assert resp.json['image_url'] == image_dict['image_url']
