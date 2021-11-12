# -*- coding: utf-8 -*-
"""User views."""
from facelo.database import db
from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required

from .models import Image
from .serializers import image_schema, image_schemas

blueprint = Blueprint("image", __name__)


@blueprint.route("/images/", methods=["POST"])
@jwt_required()
@use_kwargs(image_schema)
@marshal_with(image_schema)
def upload_image(**kwargs):
    breakpoint()
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
