# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from facelo.user.models import User


from .factories import UserFactory



@pytest.fixture
def user(db, kwargs):
    user = UserFactory(**kwargs).save()
    yield user
    user.delete()


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self, user):
        """Get user by ID."""
        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_birth_day_defaults_to_datetime(self, user):
        """Test creation date."""
        pass
        # assert bool(user.birth_day)
        # assert isinstance(user.birth_day, dt.date)

    def test_factory(self, user):
        """Test user factory."""
        assert user.id
        assert user.email
        # assert user.birth_day
        # assert user.gender != None
        # assert user.sexual_preference != None
        assert user.password

    @pytest.mark.kwargs(password='foobarbaz123')
    def test_check_password(self, user):
        """Check password."""
        assert user.check_password('foobarbaz123')
        assert not user.check_password('barfoobaz')
