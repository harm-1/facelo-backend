# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from facelo.user.models import User


from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self, db):
        """Get user by ID."""
        user = UserFactory()
        db.session.commit()
        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_birth_day_defaults_to_datetime(self):
        """Test creation date."""
        user = UserFactory()
        # assert bool(user.birth_day)
        # assert isinstance(user.birth_day, dt.date)

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert user.id
        assert user.email
        # assert user.birth_day
        # assert user.gender != None
        # assert user.sexual_preference != None
        assert user.password

    def test_check_password(self):
        """Check password."""
        user = UserFactory(password='foobarbaz123')
        assert user.check_password('foobarbaz123')
        assert not user.check_password('barfoobaz')
