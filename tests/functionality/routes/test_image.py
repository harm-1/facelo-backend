# coding: utf-8

import factory
import pytest
from conftest import header
from flask import url_for

from facelo.utils import load_image_as_string
from factories import ImageFactory


@pytest.fixture
def image_dict(user):
    image_dict = factory.build(dict, FACTORY_CLASS=ImageFactory)
    image_dict['file'] = load_image_as_string(image_dict['filename'])
    del image_dict["user"]
    return image_dict


@pytest.fixture
def upload_image(client, image_dict, user):
    image_dict["date_taken"] = str(image_dict["date_taken"])
    resp = client.post(url_for("image.upload_image"), json=image_dict, headers=header(user.token))
    yield resp


@pytest.mark.usefixtures("db")
class TestImage:

    def test_get_images(self, client, user, image):
        resp = client.get(url_for("image.get_images"), headers=header(user.token))
        assert isinstance(resp.json, list)

    def test_get_image(self, client, user, image):
        resp = client.get(url_for("image.get_image", image_id=image.id), headers=header(user.token))
        assert resp.json["file"] == load_image_as_string(image.__dict__["filename"])
        assert resp.json["id"] == image.__dict__["id"]

    def test_upload_image(self, image_dict, upload_image):
        assert upload_image.status_code == 200

    def test_update_image(self, client, user, image):
        new_date = "0015-03-17T00:00:00"
        resp = client.put(url_for("image.update_image", image_id=image.id),
                          headers=header(user.token),
                          json={"date_taken": new_date})
        assert resp.json["date_taken"] == new_date
