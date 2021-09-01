
# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user

from facelo.database import db
from .models import Image
from .serializers import image_schema, image_schemas

blueprint = Blueprint('image', __name__)


@blueprint.route('/images/', methods=['POST'])
@jwt_required()
@use_kwargs(image_schema)
@marshal_with(image_schema)
def upload_image(**kwargs):
    return Image(user=current_user, **kwargs).save()


@blueprint.route('/images/', methods=['GET'])
@jwt_required()
@marshal_with(image_schemas)
def get_images():
    return Image.query.filter_by(user=current_user).all()


@blueprint.route('/images/<image_id>', methods=['GET'])
@jwt_required()
@marshal_with(image_schema)
def get_image(image_id):
    return Image.query.filter_by(id=image_id).first()
