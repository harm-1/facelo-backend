# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user

from facelo.database import db
from .models import Challenge
from .serializers import challenge_schema, challenge_schemas

import datetime as dt
from random import shuffle, choice
from itertools import combinations
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

    to_create = generate_challenges_type(uncompleted)
    generated = generate_challenges(to_create, completed)
    created = create_challenges(generated, question)

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


def generate_challenges_type(uncompleted):
    to_create = {}
    if len(uncompleted) < 6:
        to_create = {CHALLENGE_TYPE_RANDOM: 6,
                     CHALLENGE_TYPE_SAMETRIAL: 4,
                     CHALLENGE_TYPE_TRIANGLE: 2}
    elif len(uncompleted) < 12:
        to_create = {CHALLENGE_TYPE_RANDOM: 3,
                     CHALLENGE_TYPE_SAMETRIAL: 2,
                     CHALLENGE_TYPE_TRIANGLE: 1}
    return to_create

def generate_challenges(to_create, completed):
    # I need to check that I dont send the same ones everytime
    # I think I only dont want to send the same ones in the newly created with respect to the last 50.
    generated_random = generate_random(size=to_create[CHALLENGE_TYPE_RANDOM])
    generated_sametrial = generate_sametrial(to_create[CHALLENGE_TYPE_SAMETRIAL], completed)
    generated_triangle= generate_triangle(to_create[CHALLENGE_TYPE_TRIANGLE], completed)
    generated = generated_random + generated_sametrial + generated_triangle

    # TODO test
    # TODO this can be improved
    for combo in combinations(generated, 2):
        if (combo[0]['trial_1'] == combo[1]['trial_1'] and
            combo[0]['trial_2'] == combo[1]['trial_2']) or \
            (combo[0]['trial_1'] == combo[1]['trial_2'] and
             combo[0]['trial_2'] == combo[1]['trial_1']):
            if combo[0] in generated:
                generated.remove(combo[0])
            else:
                generated.remove(combo[1])

    # now checking that they are not the same as completed challs
    # TODO test this
    for chall in completed:
        generated[:] = [
            gen_sample for gen_sample in generated if not (
                (gen_sample['trial_1'] == chall.winner_id and
                 gen_sample['trial_2'] == chall.loser_id) or
                (gen_sample['trial_1'] == chall.loser_id and
                 gen_sample['trial_2'] == chall.winner_id))
        ]
    shuffle(generated)
    return generated

def generate_random(size):
    # TODO this should actually be in the app context and then a yield functios
    # for now, lets just make it work.
    random_trials = Trial.query.order_by(sql_random()).limit(size*3).all()
    while len(random_trials) < size*3:
        random_trials.extend(Trial.query.order_by(sql_random()).all())

    generated = []
    while len(generated) < size:
        trial_1 = random_trials.pop(0)
        trial_2 = random_trials.pop(0)
        if trial_1.image.user != trial_2.image.user:
            generated.append({'type': CHALLENGE_TYPE_RANDOM, 'trial_1': trial_1, 'trial_2': trial_2})
    return(generated)

def generate_sametrial(size, completed):
    random_trials = Trial.query.order_by(sql_random()).limit(size).all()
    while len(random_trials) < size*2:
        random_trials.extend(Trial.query.order_by(sql_random()).all())

    same_trials = [chall.winner for chall in completed if chall.winner] + \
        [chall.loser for chall in completed if chall.loser]

    generated = []
    while len(generated) < size:
        trial_1 = random_trials.pop(0)
        trial_2 = choice(same_trials)
        if trial_1.image.user != trial_2.image.user:
            generated.append({'type': CHALLENGE_TYPE_RANDOM, 'trial_1': trial_1, 'trial_2': trial_2})
    return(generated)


def generate_triangle(size, completed):
    # creating the trials for no triangular winner checks
    # This functio will generate less triangular checks when they are not available.
    # Which is probably what I want. 
    winners = []
    losers = []
    for challenge in completed:
        if challenge.winner_id != None and \
           challenge.loser_id != None:
            winners.append(challenge.winner_id)
            losers.append(challenge.loser_id)

    # TODO this can be optimised, because I need only a few
    # I can probably make some yield function. 
    double_same_trials = list(set(winners).intersection(losers))
    generated = []
    for trial_id in double_same_trials:
        winner, loser = None, None
        for challenge in completed:
            if challenge.winner_id == trial_id:
                loser = challenge.loser
            if challenge.loser_id == trial_id:
                winner = challenge.winner

        if winner.image.user != loser.image.user:
            if choice([True, False]):
                generated.append({'type': CHALLENGE_TYPE_RANDOM, 'trial_1': winner, 'trial_2': loser})
            else:
                generated.append({'type': CHALLENGE_TYPE_RANDOM, 'trial_1': loser, 'trial_2': winner})


        if len(generated) == size:
            break
    return generated

def create_challenges(generated, question):
    # Now the challenges are created, it is done this way to create them in random order
    created = []
    for gen_sample in generated:
        created.append(Challenge(judge=current_user, judge_age=None, type=gen_sample['type'], \
                                 question=question, winner=gen_sample['trial_1'],
                                 loser=gen_sample['trial_2']))
    db.session.commit()
    return created




