# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest

from facelo.app import create_app
from facelo.database import db as _db
from facelo.settings import TestConfig
from facelo.user.models import User

from flask_jwt_extended import create_access_token

from .factories import UserFactory, ImageFactory


@pytest.fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()

@pytest.fixture
def kwargs(request):
    marker = request.node.get_closest_marker("kwargs")
    return marker.kwargs if marker else {}


def header(token):
    return {'Authorization': 'Bearer {}'.format(token)}

@pytest.fixture
def user_dict(kwargs):
    return UserFactory.stub(**kwargs).__dict__

@pytest.fixture
def user(db, user_dict):
    user = UserFactory(**user_dict).save()
    user.token = create_access_token(identity=user)
    yield user
    user.delete()

@pytest.fixture
def image_dict():
    return ImageFactory.stub().__dict__

@pytest.fixture
def image(db, user, image_dict):
    image = ImageFactory(user=user, **image_dict).save()
    yield image
    image.delete()
