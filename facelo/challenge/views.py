# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user

from facelo.database import db
from .models import Challenge
from .serializers import challenge_schema, challenge_schemas

import datetime as dt
from random import shuffle, choice
from collections import Counter
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
    question = Question.get_by_id(question_id)
    challenges = get_latest_challenges(question, 62)
    completed, uncompleted = sort_by_completed(challenges)

    # check 12 unfullfilled
    if len(uncompleted) > 12:
        return uncompleted

    to_create = generate_challenges_type(completed, uncompleted)
    created = create_challenges(to_create, completed, question)

    return uncompleted + created


@blueprint.route('/question/<question_id>/challenges', methods=['PUT'])
@jwt_required()
@use_kwargs(challenge_schemas)
@marshal_with(challenge_schemas)
def put_challenges(*challenges, **kwargs):
    for chall_result in challenges:
        chall_ori = Challenge.get_by_id(chall_result['id']).complete(chall_result)

    return ('', 204)



def get_latest_challenges(question, size=62):
    latest = Challenge.query.filter_by(judge=current_user, question_id=question.id) \
                            .order_by(Challenge.id.desc()).limit(size).all()
    return latest


def sort_by_completed(challenges):
    completed = []
    uncompleted = []
    for challenge in challenges:
        if challenge.completed:
            completed.append(challenge)
        else:
            uncompleted.append(challenge)
    return completed, uncompleted


def generate_challenges_type(completed, uncompleted):
    to_create = []
    if len(completed) + len(uncompleted) <= 18:
        # amount = (18-len(completed))/2
        amount = ceildiv(18-len(completed), 2)
        to_create.extend([CHALLENGE_TYPE_RANDOM] * amount + \
                         [CHALLENGE_TYPE_SAMETRIAL] * amount)

    # now there should be enough starting challenges,
    # but there might not be enough unfullfilled still
    if len(uncompleted) < 6:
        to_create.extend([CHALLENGE_TYPE_RANDOM] * 6 + \
                         [CHALLENGE_TYPE_SAMETRIAL] * 4 + \
                         [CHALLENGE_TYPE_TRIANGLE] * 2)
    elif len(uncompleted) < 12:
        to_create.extend([CHALLENGE_TYPE_RANDOM] * 3 + \
                         [CHALLENGE_TYPE_SAMETRIAL] * 2 + \
                         [CHALLENGE_TYPE_TRIANGLE] * 1)
    shuffle(to_create)
    return to_create


def create_challenges(to_create, completed, question):
    """A batch of challenges are created and saved in the db for a user"""

    counter = Counter(to_create)

    # creating a list of random trials, I might as well create them all simultaneously.
    # I some cases, when a question has very few trials, it can happen that there not enough
    # random trials. therefore it is done again.
    random_trials = Trial.query.order_by(sql_random()).limit(len(to_create)*2).all()
    if len(random_trials) < len(to_create) * 2:
        random_trials.extend(Trial.query.order_by(sql_random()).limit(len(to_create)*2).all())

    # creating the trials for no triangular winner checks
    winners = []
    losers = []
    for challenge in completed:
        winners.append(challenge.winner_id)
        losers.append(challenge.loser_id)

    # TODO if a trial gets removed it will be none, does none give an error
    # when it gets added to winners,
    # and does none interecte with none if its in the list
    # TODO this can be optimised, because I only a few
    double_same_trials = list(set(winners).intersection(losers))
    triang_trials = []
    for trial_id in double_same_trials:
        winner, loser = None, None
        for challenge in completed:
            if challenge.winner_id == trial_id:
                loser = challenge.loser
            elif challenge.loser_id == trial_id:
                winner = challenge.winner

        if (winner is not None and
            loser is not None and
            winner.image.user != loser.image.user):
            triang_trials.append((winner, loser))

        if len(triang_trials) == counter[CHALLENGE_TYPE_TRIANGLE]:
            break

    # TODO normal error checking
    assert len(triang_trials) == counter[CHALLENGE_TYPE_TRIANGLE]

    # Now the challenges are created, it is done this way to create them in random order
    created = []
    for c_type in to_create:

        # This loop is to ensure that the user isnt compared to itself
        while True:
            if c_type == CHALLENGE_TYPE_RANDOM:
                trial_1 = random_trials.pop(0)
                trial_2 = random_trials.pop(0)
            elif c_type == CHALLENGE_TYPE_SAMETRIAL:
                trial_1 = random_trials.pop(0)
                if choice([True, False]) == True:
                    trial_2 = choice(completed).winner
                else:
                    trial_2 = choice(completed).loser
            elif c_type == CHALLENGE_TYPE_TRIANGLE:
                trial_1, trial_2 = triang_trials.pop(0)

            if trial_1.image.user != trial_2.image.user:
                break

        created.append(Challenge(judge=current_user, judge_age=None, type=c_type, \
                                 question=question, winner=trial_1, loser=trial_2))

    db.session.commit()
    return created



def ceildiv(a, b):
    return -(-a // b)
