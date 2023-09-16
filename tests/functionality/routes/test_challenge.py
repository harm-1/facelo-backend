# -*- coding: utf-8 -*-
from itertools import combinations
from random import choice, sample

import pytest
from conftest import header
from flask import url_for


@pytest.fixture
def get_challenges(client, question, user):
    resp = client.get(
        url_for("challenge.get_challenges", question_id=question.id),
        headers=header(user.token),
    )
    return resp


@pytest.mark.usefixtures("db")
class TestChallenge:

    @pytest.mark.usefixtures("db", "users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize(
        "users, images, trials, questions, challenges",
        [(10, 10, 10, 1, 1)], indirect=True)
    def test_get_challenges(self, get_challenges):
        assert isinstance(get_challenges.json, list)
        if len(get_challenges.json) > 0:
            assert isinstance(get_challenges.json[0]['id'], int)
        else:
            print("Warning, no challenges created, probably bad rng")

    @pytest.mark.usefixtures("db", "users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize(
        "users, images, trials, questions, challenges",
        [(10, 20, 20, 1, 300)], indirect=True)
    def test_put_challenges(self, client, user, questions, challenges, get_challenges):
        # get_challenges gets the challenges, for each challenge a random winner is choses,
        # then the put is executed and the data will be send te the server.
        resp1 = get_challenges

        for challenge in resp1.json:
            del challenge["question_id"]
            if choice([True, False]):
                challenge["winner_id"] = challenge["loser_id"]
                challenge["loser_id"] = challenge["winner_id"]

        resp2 = client.put(url_for("challenge.put_challenges",
                                   question_id=questions[0].id),
                           headers=header(user.token),
                           json={"challenges": resp1.json})

        assert resp2.status_code == 204

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials':")
    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_delete_trial(self, db, client, trials, challenges, question, user):
        # Choose 10 trials and delete those
        # for trial in sample(trials, 10):
        #     trial.delete(commit=False)
        # db.session.commit()
        for trial in sample(trials, 10):
            trial.delete()

        resp = client.get(url_for("challenge.get_challenges", question_id=question.id), headers=header(user.token))

        assert isinstance(resp.json, list)

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials':")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'images':")
    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_delete_image(self, db, client, images, challenges, question, user):
        # Choose 10 trials and delete those
        for image in sample(images, 10):
            image.delete(commit=False)
        db.session.commit()

        resp = client.get(url_for("challenge.get_challenges", question_id=question.id), headers=header(user.token))

        assert isinstance(resp.json, list)

    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'trials':")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'images':")
    @pytest.mark.filterwarnings("ignore:DELETE statement on table 'users':")
    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)], indirect=True)
    def test_delete_user(self, db, client, users, challenges, question, user):
        # Choose 10 trials and delete those
        for user_sample in sample(users, 5):
            if user_sample != user:
                user_sample.delete(commit=False)
        db.session.commit()

        resp = client.get(url_for("challenge.get_challenges", question_id=question.id), headers=header(user.token))

        assert isinstance(resp.json, list)

    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(1, 1, 0, 1, 0), (1, 1, 1, 1, 0),
                                                                              (1, 1, 2, 1, 0), (1, 1, 3, 1, 0)],
                             indirect=True)
    def test_one_user(self, client, challenges, user, trials, question):
        resp = client.get(url_for("challenge.get_challenges", question_id=question.id), headers=header(user.token))
        assert type(resp.json) == list
        assert len(resp.json) == 0

    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(0, 0, 0, 1, 0), (1, 1, 1, 1, 0),
                                                                              (2, 2, 2, 1, 0), (3, 3, 3, 1, 0)],
                             indirect=True)
    def test_few_trials(self, client, users, challenges, user, trials, question):
        """
        This test is often failing, which is actually expected.
        The reason is that im testing that all possible challenges are getting created,
        but I create them by random selection of trials. Which is non deterministic and will somtimes cause
        not all possible challenges te be created.
        The reason that im keeping this test (for now) is that it appeared to be happening to often
        And therefore I may want to have another look at it.
        """
        resp = client.get(url_for("challenge.get_challenges", question_id=question.id), headers=header(user.token))

        user_trials_dict = {_user: 0 for _user in users}
        for _trial in trials:
            user_trials_dict[_trial.image.user] += 1

        possible_challenges_count = 0
        for _user in user_trials_dict:
            _trials_count = user_trials_dict[_user]
            possible_challenges_count += _trials_count * (len(trials) - _trials_count)

        assert type(resp.json) == list
        assert len(resp.json) == possible_challenges_count / 2
