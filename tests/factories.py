# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Faker
from factory.alchemy import SQLAlchemyModelFactory
import datetime

from facelo.database import db
from facelo.user.models import User
from facelo.image.models import Image


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

    class Meta:
        """Factory configuration."""

        model = User


class ImageFactory(BaseFactory):
    """Image factory."""

    image_url = Faker('image_url')
    created = Faker('past_datetime')
    uploaded = Faker('past_datetime')
    age_in_image = Faker('random_int', min=18, max=60)

    class Meta:
        """Factory configuration."""

        model = Image
