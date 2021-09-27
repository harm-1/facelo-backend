# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user

from facelo.database import db
from .models import Challenge
from .serializers import challenge_schema, challenge_schemas

import datetime as dt
from random import shuffle
from sqlalchemy.sql.functions import random as sql_random

blueprint = Blueprint('challenge', __name__)

from facelo.question.models import Question
from facelo.trial.models import Trial

CHALLENGE_TYPE_RANDOM = 1
CHALLENGE_TYPE_SAMETRIAL = 2
CHALLENGE_TYPE_TRIANGLE = 3


@blueprint.route('/question/<question_id>/challenges', methods=['GET'])
@jwt_required()
@marshal_with(challenge_schemas)
def get_challenges(question_id):
    challenges = get_latest_challenges(62, question_id)
    completed, uncompleted = sort_by_completed(challenges)

    # check 12 unfullfilled
    if len(uncompleted) > 12:
        return uncompleted

    # to_create = generate_challenges_type(completed, uncompleted)
    to_create = [CHALLENGE_TYPE_RANDOM] * 12
    created = create_random_challenges(to_create, question_id)

    return uncompleted + created


@blueprint.route('/question/<question_id>/challenges', methods=['PUT'])
@jwt_required()
@use_kwargs(challenge_schemas)
@marshal_with(challenge_schemas)
def put_challenges(**kwargs):
    return True


def create_random_challenges(to_create, question_id):
    # TODO maybe datetime better, but suffuces for now
    # age = dt.date.today() - current_user.birth_day
    age = None
    question = Question.get_by_id(question_id)
    challenges = []
    for c_type in to_create:
        (trial_1, trial_2) = Trial.query.order_by(sql_random()).limit(2).all()
        challenges.append(Challenge(judge=current_user, judge_age=age, type=c_type, \
                                    question=question, winner=trial_1, loser=trial_2))
    db.session.commit()
    return challenges


def sort_by_completed(challenges):
    completed = []
    uncompleted = []
    for challenge in challenges:
        if challenge.completed:
            completed.append(challenge)
        else:
            uncompleted.append(challenge)
    return completed, uncompleted

def get_latest_challenges(question_id, size=62):
    latest = Challenge.query.filter_by(judge=current_user, question_id=question_id) \
                            .order_by(Challenge.id.desc()).limit(size)
    return latest










def create_challenges(to_create):
    age = dt.datetime.utcnow() - current_user.birth_day
    question = Question.get_by_id(question_id)
    for c_type in to_create:
        if c_type == CHALLENGE_TYPE_RANDOM:
            # get one that has few hidden votes


            Challenge(judge=current_user, judge_age=age, type=c_type, \
                  question=question, )


def generate_challenges_type(completed, uncompleted):
    if len(completed) + len(uncompleted) <= 18:
        amount = (18-len(challenges))/2
        to_create = [CHALLENGE_TYPE_RANDOM] * amount + \
            [CHALLENGE_TYPE_SAMETRIAL] * amount

    # now there should be enough starting challenges,
    # but there might not be enough unfullfilled still
    if len(uncompleted) < 6:
        to_create = to_create + \
            [CHALLENGE_TYPE_RANDOM] * 6 \
            [CHALLENGE_TYPE_SAMETRIAL] * 4 \
            [CHALLENGE_TYPE_TRIANGLE] * 2
    elif len(uncompleted) < 12:
        to_create = to_create + \
            [CHALLENGE_TYPE_RANDOM] * 3 \
            [CHALLENGE_TYPE_SAMETRIAL] * 2 \
            [CHALLENGE_TYPE_TRIANGLE] * 1
    return shuffle(to_create)

