# -*- coding: utf-8 -*-
"""
This file contains code for generating challenges. A generated challenge is a dict that has two Trials and a type.
"""

from itertools import combinations
from random import choice, shuffle

from facelo.challenge.models import Challenge
from facelo.constants import (CHALLENGE_TYPE_RANDOM, CHALLENGE_TYPE_SAMETRIAL,
                              CHALLENGE_TYPE_TRIANGLE)
from facelo.trial.models import Trial
from sqlalchemy.sql.functions import random as sql_random


# TODO should be checked for lower than a number of hidden votes, but will refactor also probably
def random_trial_generator():
    if Trial.query.count() == 0:
        return None
    while True:
        trials = Trial.query.order_by(sql_random()).limit(2).all()
        # breakpoint()
        for trial in trials:
            yield trial


random_trials = random_trial_generator()


# TODO filter for trials of the user itself
# I think I only dont want to send the same ones in the newly created with respect to the last 50.
def generate_challenges(to_create: dict[int, int], uncompleted: list[Challenge],
                        completed: list[Challenge]) -> list[dict[str, int]]:
    """ This function generates data which can be used to create new challenges. Its main job is choose trials.
    The trials ca"""
    not_in_filter = created_challenges_list(uncompleted + completed)
    # generated_triangle = gen_triangle(to_create[CHALLENGE_TYPE_TRIANGLE], completed, not_in_filter)

    # not_in_filter.extend(generated_triangle)
    generated_sametrial = gen_sametrial(to_create[CHALLENGE_TYPE_SAMETRIAL], completed,
                                        not_in_filter)

    not_in_filter.extend(generated_sametrial)
    generated_random = gen_random(to_create[CHALLENGE_TYPE_RANDOM], not_in_filter)

    generated: list[dict[str, int]] = []
    for data in generated_random:
        generated.append({'trial_1': data[0], 'trial_2': data[1], 'type': CHALLENGE_TYPE_RANDOM})
    for data in generated_sametrial:
        generated.append({'trial_1': data[0], 'trial_2': data[1], 'type': CHALLENGE_TYPE_SAMETRIAL})
    # for data in generated_triangle:
    # generated.append({'trial_1': data[0], 'trial_2': data[1], 'type': CHALLENGE_TYPE_TRIANGLE})

    shuffle(generated)
    return generated


# TODO bugged, sort() returns none, trials can be none
def created_challenges_list(challenges: list[Challenge]) -> list[list[int]]:

    result = []
    for challenge in challenges:
        trials = [challenge.winner_id, challenge.loser_id]
        trials.sort(key=lambda k: (k is None, k))
        result.append(trials)

    return result

    # return [[challenge.winner_id, challenge.loser_id].sort(key=lambda k: (k is None, k))
    #         for challenge in challenges]


def gen_random(size: int, not_in_filter: list[list[int]]) -> list[list[int]]:
    """Returns a list with dictionaries with random trials. From that dictionary a challenge can be generated. If requested number of challenges cant be generated, the maximum possible will be returned."""
    generated: list[dict[str, int]] = []
    tries = 3
    while len(generated) < size and tries > 0:
        trials = [next(random_trials), next(random_trials)]
        trials.sort()
        if trials[0].image.user == trials[1].image.user or \
           trials in not_in_filter or \
           trials in generated:
            tries -= 1
            continue
        generated.append(trials)
    return generated


def gen_sametrial(size: int, completed: list[Challenge],
                  not_in_filter: list[list[int]]) -> list[list[int]]:
    if random_trials == None or len(completed) == 0:
        return []

    same_trials = [chall.winner for chall in completed if chall.winner] \
        + [chall.loser for chall in completed if chall.loser]

    generated: list[dict[str, int]] = []
    tries = 3
    while len(generated) < size:
        trials: list[list[int]] = [next(random_trials), choice(same_trials)]
        trials.sort()
        if trials[0].image.user == trials[1].image.user or \
           trials in not_in_filter or \
           trials in generated:
            tries -= 1
            continue
        generated.append(trials)
    return generated


def gen_triangle(size: int, completed: list[Challenge],
                 not_in_filter: list[list[int]]) -> list[dict[str, int]]:
    # creating the trials for no triangular winner checks
    # This functio will generate less triangular checks when they are not available.
    # Which is probably what I want.
    winners = []
    losers = []
    for challenge in completed:
        if challenge.winner_id != None and challenge.loser_id != None:
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

        trials = [winner, loser]
        trials.sort()
        if winner.image.user != loser.image.user and \
           trials not in not_in_filter and \
           trials not in generated:
            generated.append(trials)

        if len(generated) == size:
            break
    return generated
