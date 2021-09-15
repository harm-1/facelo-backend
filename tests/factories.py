# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Faker, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
import datetime

from facelo.database import db
from facelo.user.models import User
from facelo.image.models import Image
from facelo.trial.models import Trial
from facelo.question.models import Question
from facelo.challenge.models import Challenge


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    email = Faker('email')
    password = Faker('password')
    birth_day = Faker(
        'date_between_dates',
        date_start=datetime.date(1900, 1, 1),
        date_end=datetime.date(2020, 1, 1))
    gender = Faker('random_int', min=0, max=2)
    sexual_preference = Faker('random_int', min=0, max=7)
    karma = Faker('random_int', min=0, max=300)

    class Meta:
        """Factory configuration."""

        model = User


class ImageFactory(BaseFactory):
    """Image factory."""

    image_url = Faker('image_url')
    date_taken = Faker('past_datetime')

    # user = SubFactory(UserFactory)

    class Meta:
        """Factory configuration."""

        model = Image

class TrialFactory(BaseFactory):
    """Trial factory."""

    score = Faker('pyfloat', min_value=0, max_value=1)
    judge_age_min = Faker('random_int', min=0, max=50)
    judge_age_max = Faker('random_int', min=51, max=100)

    class Meta:
        """Factory configuration."""

        model = Trial

class QuestionFactory(BaseFactory):
    """Question factory."""

    question = Faker('sentence', nb_words=10)

    class Meta:
        """Factory configuration."""

        model = Question

class ChallengeFactory(BaseFactory):
    """Challenge factory."""

    judge_age = Faker('random_int', min=18, max=70)
    date = Faker('past_datetime')
    type = Faker('random_int', min=0, max=5)
    winner_has_revealed = Faker('boolean')
    loser_has_revealed = Faker('boolean')
    completed = Faker('boolean')


    class Meta:
        """Factory configuration."""

        model = Challenge
