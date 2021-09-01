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
def image_dict():
    image_dict = ImageFactory.stub().__dict__
    image_dict['created'] = str(image_dict['created'])
    image_dict['uploaded'] = str(image_dict['uploaded'])
    return image_dict

@pytest.fixture
def upload_image(client, image_dict, register_user):
    token = str(register_user.json['token'])
    # breakpoint()
    resp = client.post(url_for("image.upload_image"), json=image_dict, headers={
        'Authorization': 'Bearer {}'.format(token)})
    return resp



@pytest.mark.usefixtures('db')
class TestImage:

    def test_get_images(self, client, register_user, image_dict, upload_image):
        token = str(register_user.json['token'])
        resp = client.get(url_for('image.get_images'), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert(isinstance(resp.json, list))

    # def test_get_image(self, client, register_user, image_dict, upload_image):
    #     token = str(register_user.json['token'])
    #     image_id = image_dict.id
    #     resp = client.get(url_for('image.get_image/{}'.format(image_id)),
    #                       headers={'Authorization': 'Bearer {}'.format(token)})
    #     assert resp.json['image_url'] == image_dict['image_url']
