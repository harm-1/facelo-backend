# coding: utf-8

import factory
import pytest
from flask import url_for

from .conftest import header
from .factories import TrialFactory


@pytest.fixture
def trial_dict():
    trial_dict = factory.build(dict, FACTORY_CLASS=TrialFactory)
    del trial_dict['image']
    del trial_dict['question']
    return trial_dict

@pytest.mark.usefixtures('db')
class TestTrial:

    def test_get_trials(self, client, user, image, trial):
        resp = client.get(url_for('trial.get_trials', image_id=image.id),
                          headers=header(user.token))
        assert(isinstance(resp.json, list))

    def test_get_trial(self, client, user, image, trial):
        resp = client.get(url_for('trial.get_trial', image_id=image.id,
                                  trial_id=trial.id),
                          headers=header(user.token))
        assert resp.json['id'] == trial.__dict__['id']

    def test_upload_trial(self, client, user, image, question, trial_dict):
        del trial_dict['score']
        resp = client.post(url_for("trial.create_trial", image_id=image.id,
                                   question_id=question.id), json=trial_dict,
                           headers=header(user.token))
        assert resp.json['judge_age_min'] == trial_dict['judge_age_min']
        assert resp.json['judge_age_max'] == trial_dict['judge_age_max']

    # @pytest.mark.trial_kwargs(judge_age_min=42, judge_age_max=69)
    # @pytest.mark.parametrize("data,status_code", [
    #     ({'judge_age_min': 42, 'judge_age_max': 69}, 200),
    #     ({'judge_age_min': 69, 'judge_age_max': 42}, 422),])
    # def test_update_trial(self, client, user, image, trial, data, status_code):
    #     resp = client.put(url_for('trial.update_trial', image_id=image.id,
    #                               trial_id=trial.id),
    #                       headers=header(user.token), json=data)
    #     assert resp.status_code == status_code
