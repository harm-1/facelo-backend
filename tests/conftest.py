# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import factory
import pytest

from facelo.app import create_app
from facelo.database import db as _db
from facelo.settings import TestConfig
from factories import (ChallengeFactory, ImageFactory, QuestionFactory,
                       TrialFactory, UserFactory)


@pytest.fixture(scope="function")
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def cleanup(app):
    yield None
    import os
    from importlib import reload

    from facelo.challenge import generate

    # This is done to reset the random_trials variable
    generate = reload(generate)

    assert os.environ.get('IMAGES_DIR') == 'testing_images'
    for root, _, files in os.walk(app.config['IMAGES_DIR']):
        for _file in files:
            os.remove(os.path.join(root, _file))


# @pytest.fixture(scope='class')
@pytest.fixture()
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
def user_dict(request):
    if hasattr(request, "param"):
        return factory.build(dict, FACTORY_CLASS=UserFactory, **request.param)
    return factory.build(dict, FACTORY_CLASS=UserFactory)


@pytest.fixture
def user(db, user_dict):
    user = UserFactory(**user_dict).save()
    user.create_access_token()
    yield user
    user.delete()


@pytest.fixture
def image(user):
    image = ImageFactory(user=user).save()
    yield image
    image.delete()


@pytest.fixture
def question():
    question = QuestionFactory().save()
    yield question


@pytest.fixture
def trial(image, question):
    trial = TrialFactory(image=image, question=question).save()
    yield trial
    trial.delete()


@pytest.fixture
def losing_trial(image, question):
    trial = TrialFactory(image=image, question=question).save()
    yield trial
    trial.delete()


@pytest.fixture
def challenge(user, question, trial, losing_trial):
    challenge = ChallengeFactory(judge=user, question=question).save()
    challenge.update(winner_id=trial.id, loser_id=losing_trial.id)
    yield challenge
