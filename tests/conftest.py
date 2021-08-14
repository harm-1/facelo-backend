# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest

from facelo.app import create_app
from facelo.database import db as _db
from facelo.settings import TestConfig
from facelo.user.models import User


from .factories import UserFactory


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


# @pytest.fixture
# def user(db):
#     """A user for the tests."""
#     class User():
#         def get(self):
#             muser = UserFactory(password='myprecious')
#             muser.save()
#             db.session.commit()
#             return muser
#     return User()

@pytest.fixture
def kwargs(request):
    marker = request.node.get_closest_marker("kwargs")
    return marker.kwargs if marker else {}
