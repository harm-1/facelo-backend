# -*- coding: utf-8 -*-
"""factories to help in tests."""
import datetime
import uuid
import os
import shutil
from random import choice

import factory
from facelo.challenge.models import Challenge
from facelo.database import db
from facelo.image.models import Image
from facelo.question.models import Question
from facelo.trial.models import Trial
from facelo.user.models import User
from factory import Faker, LazyFunction, LazyAttribute, PostGeneration, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from flask_jwt_extended import create_access_token
from facelo.constants import ALLOWED_IMAGE_EXTENSIONS


class BaseFactory(SQLAlchemyModelFactory):
    """base factory."""

    class Meta:
        """factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    email = Faker("email")
    password = Faker("password")
    birth_day = Faker(
        "date_between_dates",
        date_start=datetime.date(1900, 1, 1),
        date_end=datetime.date(2020, 1, 1),
    )
    gender = Faker("random_int", min=0, max=2)
    sexual_preference = Faker("random_int", min=0, max=7)
    karma = Faker("random_int", min=0, max=300)

    # token = postgeneration(lambda obj, create, extracted, **kwargs: obj.create_access_token()
    #                        if hasattr(obj, 'create_access_token') else none)
    # token = postgenerationmethodcall('create_access_token')

    class Meta:
        """factory configuration."""

        model = User


def lazy_users():
    """turn `User.query.all()` into a lazily evaluated generator"""
    while True:
        user_list = User.query.all()
        yield choice(user_list) if user_list else none


def save_image():
    # i have to choose a random Image from example_Images and save that in testing_Images
    random_image = '/backend/example_images/{}'.format(choice(os.listdir('example_images')))

    # create filename
    filename = '{}.{}'.format(uuid.uuid4().hex, choice(list(ALLOWED_IMAGE_EXTENSIONS)))
    filepath = '/backend/testing_images/{}'.format(filename)

    # save it
    shutil.copy(random_image, filepath)

    return filename


class ImageFactory(BaseFactory):
    """Image factory."""

    # filename = Faker("file_name", category='Image')
    filename = LazyFunction(save_image)
    date_taken = Faker("past_datetime")
    user = factory.Iterator(lazy_users())

    class Meta:
        """Factory configuration."""

        model = Image


def lazy_images():
    while True:
        yield choice(Image.query.all())


class QuestionFactory(BaseFactory):
    """Question factory."""

    Question = Faker("sentence", nb_words=10)

    class Meta:
        """Factory configuration."""

        model = Question


def lazy_questions():
    while True:
        yield choice(Question.query.all())


class TrialFactory(BaseFactory):
    """Trial factory."""

    score = Faker("pyfloat", min_value=0, max_value=1)
    judge_age_min = Faker("random_int", min=1, max=50)
    judge_age_max = Faker("random_int", min=51, max=100)
    Image = factory.Iterator(lazy_images())
    question = factory.Iterator(lazy_questions())

    class Meta:
        """Factory configuration."""

        model = Trial


def lazy_trials():
    curr = None
    while True:
        prev = curr
        while prev == curr:
            curr = choice(Trial.query.all())
        yield curr


class ChallengeFactory(BaseFactory):
    """Challenge factory."""

    judge_age = Faker("random_int", min=18, max=70)
    date = Faker("past_datetime")
    type = Faker("random_int", min=0, max=5)
    winner_has_revealed = Faker("boolean")
    loser_has_revealed = Faker("boolean")
    completed = Faker("boolean")
    judge = factory.Iterator(lazy_users())
    question = factory.Iterator(lazy_questions())
    winner = factory.Iterator(lazy_trials())
    loser = factory.Iterator(lazy_trials())

    class Meta:
        """Factory configuration."""

        model = Challenge
