# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import base64
import os
import uuid

from flask import current_app

from facelo.user.models import User  # noqa


def jwt_identity(payload):
    return User.get_by_id(payload)


def identity_loader(user):
    return user.id


def save_image(image: str, filename: str):
    filename = '{}.{}'.format(uuid.uuid4().hex, filename.rsplit('.', 1)[1])
    with open(image_path(filename), "wb") as file:
        file.write(base64.b64decode(image))
    return filename


def load_image_as_string(filename: str) -> str:
    return _load_image_as_string(image_path(filename))


def _load_image_as_string(filepath: str) -> str:
    with open(filepath, "rb") as image2string:
        # Encode to base 64, that is a string representation of the data.
        # Then decode to utf-8, because I cant send data of type 'bytes' over json
        image_str = base64.b64encode(image2string.read()).decode('utf-8')
    return image_str


def image_path(filename: str) -> str:
    return os.path.join(current_app.config['IMAGES_DIR'], filename)
