# -*- coding: utf-8 -*-
"""User views."""
import base64
import uuid

from flask import Blueprint, current_app, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required

from facelo.database import db

from .models import Image
from .serializers import image_schema, image_schemas

blueprint = Blueprint("image", __name__)


@blueprint.route("/images/", methods=["POST"])
@jwt_required()
@use_kwargs(image_schema)
@marshal_with(image_schema)
def upload_image(**kwargs):
    return Image(user=current_user, **kwargs).save()


@blueprint.route("/images/", methods=["GET"])
@jwt_required()
@marshal_with(image_schemas)
def get_images():
    return Image.query.filter_by(user=current_user).all()


@blueprint.route("/images/<image_id>", methods=["GET"])
@jwt_required()
@marshal_with(image_schema)
def get_image(image_id):
    return Image.query.filter_by(id=image_id).first()


@blueprint.route("/images/<image_id>", methods=["PUT"])
@jwt_required()
@use_kwargs(image_schema)
@marshal_with(image_schema)
def update_image(image_id, **kwargs):
    image = Image.query.filter_by(id=image_id).first()
    image.update(**kwargs)
    return image


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(image: str, filename: str):

    filename = '{}.{}'.format(uuid.uuid4().hex, filename.rsplit('.', 1)[1])
    filepath = '{}/{}'.format(current_app.config['IMAGES_DIR'], filename)

    # TODO use werkzeug save
    with open(filepath, "wb") as file:
        file.write(base64.b64decode(image))

    return filename


def load_image_as_string(filename: str):

    with open(filename, "rb") as image2string:
        image_str = base64.b64encode(image2string.read())

    return image_str
