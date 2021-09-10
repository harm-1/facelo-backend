# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest

from facelo.app import create_app
from facelo.database import db as _db
from facelo.settings import TestConfig

from flask_jwt_extended import create_access_token

from .factories import UserFactory, ImageFactory, TrialFactory, QuestionFactory


@pytest.fixture(scope='session')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='class')
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
def image(user, image_dict):
    image = ImageFactory(user=user, **image_dict).save()
    yield image
    image.delete()

@pytest.fixture
def question_dict():
    return QuestionFactory.stub().__dict__

@pytest.fixture
def question(question_dict):
    question = QuestionFactory(**question_dict).save()
    yield question
    question.delete()

@pytest.fixture
def trial_kwargs(request):
    marker = request.node.get_closest_marker("trial_kwargs")
    return marker.kwargs if marker else {}

@pytest.fixture
def trial_dict(trial_kwargs):
    return TrialFactory.stub(**trial_kwargs).__dict__

@pytest.fixture
def trial(image, question, trial_dict):
    trial = TrialFactory(image=image, question=question, **trial_dict).save()
    yield trial
    trial.delete()
