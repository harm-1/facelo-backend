# coding: utf-8

import factory
import pytest
from conftest import header
from flask import url_for

from factories import ImageFactory


@pytest.fixture
def image_dict():
    image_dict = factory.build(dict, FACTORY_CLASS=ImageFactory)
    del image_dict["user"]
    return image_dict


# TODO this should actually upload a file
@pytest.fixture
def upload_image(client, image_dict, user):
    image_dict["date_taken"] = str(image_dict["date_taken"])
    image_dict['filename'] = next(image_dict['filename'])

    resp = client.post(url_for("image.upload_image"), json=image_dict, headers=header(user.token))
    yield resp


@pytest.mark.usefixtures("db")
class TestImage:

    def test_get_images(self, client, user, image):
        resp = client.get(url_for("image.get_images"), headers=header(user.token))
        assert isinstance(resp.json, list)

    def test_get_image(self, client, user, image):
        resp = client.get(url_for("image.get_image", image_id=image.id), headers=header(user.token))
        assert resp.json["filename"] == image.__dict__["filename"]

    def test_upload_image(self, image_dict, upload_image):
        assert upload_image.json["filename"] == image_dict["filename"]

    def test_update_image(self, client, user, image):
        new_date = "0015-03-17T00:00:00"
        resp = client.put(
            url_for("image.update_image", image_id=image.id),
            headers=header(user.token),
            json={"date_taken": new_date},
        )
        assert resp.json["date_taken"] == new_date
