# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, create_access_token, current_user
from sqlalchemy.exc import IntegrityError

from facelo.database import db
from facelo.exceptions import InvalidUsage
from .models import User
from .serializers import user_schema

blueprint = Blueprint('user', __name__)


@blueprint.route('/user', methods=['POST'])
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(password, email, **kwargs):
    try:
        user = User(email, password=password, **kwargs).save()
        user.token = create_access_token(identity=user)
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    return user


@blueprint.route('/user/login', methods=['POST'])
@jwt_required(optional=True)
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        raise InvalidUsage.user_not_found()


@blueprint.route('/user', methods=['GET'])
@jwt_required()
@marshal_with(user_schema)
def get_user():
    return current_user


@blueprint.route('/user', methods=['PUT'])
@jwt_required()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    user = current_user
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    return user
