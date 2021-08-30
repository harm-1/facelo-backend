# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from facelo.user.models import User
from facelo.image.models import Image


from .factories import UserFactory, ImageFactory

@pytest.fixture
def user(db, kwargs):
    user = UserFactory(**kwargs).save()
    yield user
    user.delete()

@pytest.fixture
def image(db):
    image = ImageFactory().save()
    yield image
    image.delete()

@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self, user):
        """Get user by ID."""
        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_birth_day_defaults_to_datetime(self, user):
        """Test creation date."""
        assert bool(user.birth_day)
        assert isinstance(user.birth_day, dt.date)

    def test_factory(self, user):
        """Test user factory."""
        assert user.id
        assert user.email
        assert user.birth_day
        assert user.gender != None
        assert user.sexual_preference != None
        assert user.password

    @pytest.mark.kwargs(password='foobarbaz123')
    def test_check_password(self, user):
        """Check password."""
        assert user.check_password('foobarbaz123')
        assert not user.check_password('barfoobaz')


@pytest.mark.usefixtures('db')
class TestImage:

    def test_get_by_id(self, image):
        """Get user by ID."""
        retrieved = Image.get_by_id(image.id)
        assert retrieved == image

    def test_defaults_to_datetime(self, image):
        """Test creation date."""
        assert bool(image.created)
        assert bool(image.uploaded)
        assert isinstance(image.created, dt.datetime)
        assert isinstance(image.uploaded, dt.datetime)

    def test_factory(self, image):
        """Test user factory."""
        assert image.id
        assert image.image_url
        assert image.created
        assert image.uploaded
        assert image.age_in_image

