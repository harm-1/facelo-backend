# -*- coding: utf-8 -*-
import pytest
from random import choice

from .factories import (UserFactory, ImageFactory, TrialFactory, QuestionFactory,
                        ChallengeFactory)

# from facelo.user.models import User
# from facelo.image.models import Image
# from facelo.trial.models import Trial
# from facelo.question.models import Question
# from facelo.challenge.models import Challenge










@pytest.fixture
def users(db, kwargs):
    users = UserFactory.create_batch(size=kwargs['no_users'])
    db.session.commit()
    for user in users:
        user.create_access_token()
    db.session.commit()
    yield users
    # for user in users:
    #     user.delete(commit=False)
    # db.session.commit()

@pytest.fixture
def images(db, kwargs, users):
    images = ImageFactory.create_batch(size=kwargs['no_images'])
    for image in images:
        image.user = choice(users)
    db.session.commit()
    yield images
    # for image in images:
    #     image.delete(commit=False)
    # db.session.commit()

@pytest.fixture
def questions(db, kwargs):
    questions = QuestionFactory.create_batch(size=kwargs['no_questions'])
    db.session.commit()
    yield questions
    # for question in questions:
    #     question.delete(commit=False)
    # db.session.commit()

@pytest.fixture
def trials(db, kwargs, images, questions):
    trials = TrialFactory.create_batch(size=kwargs['no_trials'])
    for trial in trials:
        trial.image = choice(images)
        trial.question = choice(questions)
    db.session.commit()
    yield trials
    for trial in trials:
        trial.delete(commit=False)
    db.session.commit()

@pytest.fixture
def challenges(db, kwargs, users, trials, questions):
    challenges = ChallengeFactory.create_batch(size=kwargs['no_challenges'])
    for challenge in challenges:
        challenge.judge = choice(users)
        challenge.question = choice(questions)
        challenge.winner = choice(trials)
        challenge.loser = choice(trials)
    db.session.commit()
    yield challenges
    # for challenge in challenges:
    #     challenge.delete(commit=False)
    # db.session.commit()




@pytest.mark.usefixtures('db')
class TestBig:
    """User tests."""

    # @pytest.mark.kwargs(no_users=10, no_images=20, no_trials=20, no_questions=1, no_challenges=300)
    # def test_delete_trial(self, db, trials, challenges):
    #     trial = choice(trials)
    #     image = trial.image
    #     challenges = trial.challenges
    #     question = trial.question
    #     trial.delete()
    #     assert trial not in image.trials
    #     assert trial not in question.trials
    #     for challenge in challenges:
    #         assert challenge.winner != trial
    #         assert challenge.loser != trial
