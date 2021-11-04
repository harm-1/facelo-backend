# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest
from facelo.challenge.models import Challenge
from facelo.image.models import Image
from facelo.question.models import Question
from facelo.trial.models import Trial
from facelo.user.models import User


@pytest.mark.usefixtures("db")
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
        assert user.karma != None

    @pytest.mark.parametrize("user_dict", [{"password": "foobarbaz123"}], indirect=True)
    def test_check_password(self, user_dict, user):
        """Check password."""
        assert user.check_password("foobarbaz123")
        assert not user.check_password("barfoobaz")

    def test_relations(self, user, image):
        assert image in user.images

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials' expected to delete:")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'images' expected to delete:")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'users' expected to delete:")
    def test_delete(self, user, image):
        user.delete()
        assert Image.get_by_id(image.id) == None


@pytest.mark.usefixtures("db")
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

    def test_relations(self, user, image, trial):
        assert image.user == user
        assert trial in image.trials

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials' expected to delete:")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'images' expected to delete:")
    def test_delete(self, user, image, trial):
        image.delete()
        assert image not in user.images
        assert Trial.get_by_id(trial.id) == None


@pytest.mark.usefixtures("db")
class TestTrial:

    def test_get_by_id(self, trial):
        retrieved = Trial.get_by_id(trial.id)
        assert retrieved == trial

    def test_factory(self, trial):
        assert trial.id
        assert trial.judge_age_min
        assert trial.judge_age_max

    def test_relations(self, image, trial, question, challenge):
        assert trial.image == image
        assert trial.question == question
        assert challenge in trial.challenges

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials' expected to delete:")
    def test_delete(self, image, trial, challenge, question):
        trial.delete()
        assert trial not in image.trials
        assert trial not in question.trials
        assert challenge.winner != trial
        assert challenge.loser != trial


@pytest.mark.usefixtures("db")
class TestQuestion:

    def test_get_by_id(self, question):
        retrieved = Question.get_by_id(question.id)
        assert retrieved == question

    def test_factory(self, question):
        assert question.id
        assert question.question

    def test_relations(self, trial, question, challenge):
        assert challenge in question.challenges
        assert trial in question.trials


@pytest.mark.usefixtures("db")
class TestChallenge:

    def test_get_by_id(self, challenge):
        retrieved = Challenge.get_by_id(challenge.id)
        assert retrieved == challenge

    def test_factory(self, challenge):
        assert challenge.id
        assert challenge.judge_age
        assert challenge.date
        assert challenge.type != None
        assert challenge.winner_has_revealed != None
        assert challenge.loser_has_revealed != None
        assert challenge.completed != None

    def test_defaults_to_datetime(self, challenge):
        """Test creation date."""
        assert bool(challenge.date)
        assert isinstance(challenge.date, dt.datetime)

    def test_relations(self, user, trial, losing_trial, question, challenge):
        assert challenge.winner == trial
        assert challenge.loser == losing_trial
        assert challenge.question == question
        assert challenge.judge == user
