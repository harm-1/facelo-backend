# -*- coding: utf-8 -*-
import pytest
from random import choice, sample
from flask import url_for

from .conftest import header
from .factories import (UserFactory, ImageFactory, TrialFactory, QuestionFactory,
                        ChallengeFactory)

@pytest.fixture
def users(db, user, request):
    # This fixture uses the user fixture, because I pass data to that fixture. So that
    # I have a user that I can log into
    # I subtract 1 to compensate for the user
    size = request.param if hasattr(request, 'param') else 10
    users = UserFactory.create_batch(size=size-1)
    db.session.commit()
    for new_user in users:
        new_user.create_access_token()
    db.session.commit()
    # I yield the user and the users in one list
    yield [user] + users
    for new_user in users:
        new_user.delete(commit=False)
    db.session.commit()

@pytest.fixture
def images(db, image, request, users):
    size = request.param if hasattr(request, 'param') else 20
    images = ImageFactory.create_batch(size=size-1)
    for new_image in images:
        new_image.user = choice(users)
    db.session.commit()
    yield [image] + images
    for new_image in images:
        new_image.delete(commit=False)
    db.session.commit()

@pytest.fixture
def questions(db, question, request):
    size = request.param if hasattr(request, 'param') else 1
    questions = QuestionFactory.create_batch(size=size-1)
    db.session.commit()
    yield [question] + questions
    # I wont remove questions ever for data consistancy
    # So I wont remove them here

@pytest.fixture
def trials(db, trial, request, images, questions):
    size = request.param if hasattr(request, 'param') else 20
    trials = TrialFactory.create_batch(size=size-1)
    for new_trial in trials:
        new_trial.image = choice(images)
        new_trial.question = choice(questions)
    db.session.commit()
    yield [trial] + trials
    for new_trial in trials:
        new_trial.delete(commit=False)
    db.session.commit()

@pytest.fixture
def challenges(db, request, users, trials, questions):
    size = request.param if hasattr(request, 'param') else 300
    challenges = ChallengeFactory.create_batch(size=size, completed=True)
    for challenge in challenges:
        challenge.judge = choice(users)
        challenge.question = choice(questions)
        challenge.winner = choice(trials)
        challenge.loser = choice(trials)
        while challenge.loser == challenge.winner:
            challenge.loser = choice(trials)

    db.session.commit()
    yield challenges
    # I wont remove challenges ever for data consistancy
    # So I wont remove them here





@pytest.fixture
def get_challenges(client, question, user):
    resp = client.get(url_for('challenge.get_challenges',
                                  question_id=question.id),
                          headers=header(user.token))
    return resp

"""
    Ik moet meer tests hebben, en ik moet er ff over denken wat voor tests ik nodig heb.

    - Ik moet testen voor het geval dat er weinig trials zijn.
      Voor elke hoeveel onder een bepaalde waarde waarschijnlijk. Ik moet checken of er wel goede
      challenges gemaakt worden voor het geval er kleine hoeveelheden trials beschibaar zijn.
    - Ik moet testen of er dan niet dezelfde challenges worden gemaakt.
    - Ik denk dat ik helemaal niet dezelfde challenges wil (in korte tijd)
      Dus ik moet daar een check voor maken bij het creeren.
      Maar dat doe ik misschien wel als ik tests met weinig trials maak. 

"""



@pytest.mark.usefixtures('db')
class TestBig:

    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_get_challenges(self, challenges, get_challenges):
        assert(isinstance(get_challenges.json, list))

    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_put_challenges(self, client, user, questions, challenges, get_challenges):
        resp1 = get_challenges
        for challenge in resp1.json:
            del challenge['question_id']
            if choice([True, False]) == True:
                challenge['winner_id'] = challenge['loser_id']
                challenge['loser_id'] = challenge['winner_id']

        resp2 = client.put(url_for('challenge.put_challenges', question_id=questions[0].id),
                           headers=header(user.token), json={'challenges':resp1.json})

        assert resp2.status_code == 204


    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials' expected to delete:")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_delete_trial(self, db, client, trials, challenges, question, user):
        # Choose 10 trials and delete those
        for trial in sample(trials, 10):
            trial.delete(commit=False)
        db.session.commit()

        resp = client.get(url_for('challenge.get_challenges',
                                  question_id=question.id),
                          headers=header(user.token))

        assert(isinstance(resp.json, list))

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials' expected to delete:")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'images' expected to delete:")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_delete_image(self, db, client, images, challenges, question, user):
        # Choose 10 trials and delete those
        for image in sample(images, 10):
            image.delete(commit=False)
        db.session.commit()

        resp = client.get(url_for('challenge.get_challenges',
                                  question_id=question.id),
                          headers=header(user.token))

        assert(isinstance(resp.json, list))

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials' expected to delete:")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'images' expected to delete:")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'users' expected to delete:")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_delete_user(self, db, client, users, challenges, question, user):
        # Choose 10 trials and delete those
        for user_sample in sample(users, 5):
            if user_sample != user:
                user_sample.delete(commit=False)
        db.session.commit()

        resp = client.get(url_for('challenge.get_challenges',
                                  question_id=question.id),
                          headers=header(user.token))

        assert(isinstance(resp.json, list))

    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(1, 1, 1, 1, 0)], indirect=True)
    def test_few_trials(self, client, challenges, user, question):
        resp = client.get(url_for('challenge.get_challenges',
                                  question_id=question.id),
                          headers=header(user.token))

        assert(resp.json == [])
