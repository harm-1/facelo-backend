# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from facelo.user.models import User
from facelo.image.models import Image
from facelo.trial.models import Trial


from .factories import UserFactory, ImageFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self, user):
        """Get user by ID."""
        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_birth_day_defaults_to_date(self, user):
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
        assert user.karma

    @pytest.mark.kwargs(password='foobarbaz123')
    def test_check_password(self, user):
        """Check password."""
        assert user.check_password('foobarbaz123')
        assert not user.check_password('barfoobaz')


@pytest.mark.usefixtures('db')
class TestImage:

    def test_get_by_id(self, image):
        retrieved = Image.get_by_id(image.id)
        assert retrieved == image

    def test_defaults_to_datetime(self, image):
        """Test creation date."""
        assert bool(image.created)
        assert bool(image.date_taken)
        assert isinstance(image.created, dt.datetime)
        assert isinstance(image.date_taken, dt.datetime)

    def test_factory(self, image):
        """Test user factory."""
        assert image.id
        assert image.image_url
        assert image.created
        assert image.date_taken


@pytest.mark.usefixtures('db')
class TestTrial:

    def test_get_by_id(self, trial):
        retrieved = Trial.get_by_id(trial.id)
        assert retrieved == trial

    def test_factory(self, trial):
        assert trial.id
        assert trial.judge_age_min
        assert trial.judge_age_max
