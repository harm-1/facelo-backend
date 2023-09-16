# -*- coding: utf-8 -*-
"""
This file contains code for generating challenges. A generated challenge is a dict that has two Trials and a type.
"""
from collections.abc import Generator
from itertools import combinations
from random import choice, shuffle
from typing import Optional

from sqlalchemy.sql.functions import random as sql_random

from facelo.challenge.models import Challenge
from facelo.constants import (CHALLENGE_TYPE_RANDOM, CHALLENGE_TYPE_SAMETRIAL,
                              CHALLENGE_TYPE_TRIANGLE, RANDOM_TRIALS_COUNT)
from facelo.trial.models import Trial
from facelo.user.models import User


def random_trial_generator() -> Optional[Generator[Trial, None, None]]:
    """
    When new challenges need to be created for an user,
    we need to get multple random trials.
    We use a generator because this way we only have to do one query.
    """
    if Trial.query.count() == 0:
        return None
    while True:
        trials = Trial.query.order_by(
            sql_random()).limit(RANDOM_TRIALS_COUNT).all()
        for trial in trials:
            yield trial


random_trials = random_trial_generator()


def generate_challenges(to_create: dict[int, int],
                        uncompleted: list[Challenge],
                        completed: list[Challenge],
                        user: User) -> list[dict[str, int]]:
    """ This function generates data which can be used to create new challenges.
    Its main job is choose trials.
    The trials ca"""
    not_in_filter = created_challenges_list(uncompleted + completed)
    generated_triangle = gen_triangle(to_create[CHALLENGE_TYPE_TRIANGLE],
                                      completed, user, not_in_filter)

    not_in_filter.extend(generated_triangle)
    generated_sametrial = gen_sametrial(to_create[CHALLENGE_TYPE_SAMETRIAL],
                                        completed, user, not_in_filter)

    not_in_filter.extend(generated_sametrial)
    generated_random = gen_random(to_create[CHALLENGE_TYPE_RANDOM], user,
                                  not_in_filter)

    generated: list[dict[str, int]] = []
    for data in generated_random:
        generated.append({
            'trial_1': data[0],
            'trial_2': data[1],
            'type': CHALLENGE_TYPE_RANDOM
        })
    for data in generated_sametrial:
        generated.append({
            'trial_1': data[0],
            'trial_2': data[1],
            'type': CHALLENGE_TYPE_SAMETRIAL
        })
    for data in generated_triangle:
        generated.append({
            'trial_1': data[0],
            'trial_2': data[1],
            'type': CHALLENGE_TYPE_TRIANGLE
        })

    shuffle(generated)
    return generated


# TODO: this function exists because I created the challenge model in
# such a way that the winner and loser fields are filled with the candidates
# so they are not the actuall winner, the challenge is not completed yet.
# I did this to save diskspace, which is complete;y pointless
def created_challenges_list(challenges: list[Challenge]) -> list[list[Trial]]:
    return [
        sorted([challenge.winner, challenge.loser],
               key=lambda k: (k is None, k)) for challenge in challenges
    ]


def gen_random(size: int, user: User,
               not_in_filter: list[list[Trial]]) -> list[list[Trial]]:
    """Returns a list with dictionaries with random trials.
    From that dictionary a challenge can be generated.
    If requested number of challenges cant be generated,
    the maximum possible will be returned."""
    generated: list[list[Trial]] = []
    tries = 3
    while len(generated) < size and tries > 0:
        trials = sorted([next(random_trials), next(random_trials)])
        if trials[0].image.user == trials[1].image.user or \
           trials[0].image.user == user or trials[1].image.user == user or \
           trials in not_in_filter or \
           trials in generated:
            tries -= 1
            continue
        generated.append(trials)
    return generated


def gen_sametrial(size: int, completed: list[Challenge], user: User,
                  not_in_filter: list[list[Trial]]) -> list[list[Trial]]:
    if random_trials == None or len(completed) == 0:
        return []

    same_trials = [chall.winner for chall in completed if chall.winner] \
        + [chall.loser for chall in completed if chall.loser]

    if len(same_trials) == 0:
        return []

    generated: list[list[Trial]] = []
    tries = 3
    while len(generated) < size and tries > 0:
        trials: list[list[Trial]] = sorted(
            [next(random_trials), choice(same_trials)])
        if trials[0].image.user == trials[1].image.user or \
           trials[0].image.user == user or trials[1].image.user == user or \
           trials in not_in_filter or \
           trials in generated:
            tries -= 1
            continue
        generated.append(trials)
    return generated


def gen_triangle(size: int, completed: list[Challenge], user: User,
                 not_in_filter: list[list[Trial]]) -> list[list[Trial]]:
    # creating the trials for no triangular winner checks
    # This functio will generate less triangular checks when they are not available.
    # Which is probably what I want.
    winners = []
    losers = []
    for challenge in completed:
        if challenge.winner_id != None and challenge.loser_id != None:
            winners.append(challenge.winner)
            losers.append(challenge.loser)

    # TODO this can be optimised, because I need only a few
    # I can probably make some yield function.
    double_same_trials = list(set(winners).intersection(losers))
    generated = []
    for trial in double_same_trials:
        winner, loser = None, None
        for challenge in completed:
            if challenge.winner == trial:
                loser = challenge.loser
            if challenge.loser == trial:
                winner = challenge.winner

        trials = sorted([winner, loser])
        if trials[0].image.user == trials[1].image.user or \
           trials[0].image.user == user or trials[1].image.user == user or \
           trials in not_in_filter or \
           trials in generated:
            continue

        generated.append(trials)
        if len(generated) == size:
            break
    return generated
