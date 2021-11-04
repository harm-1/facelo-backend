# -*- coding: utf-8 -*-
"""
This file contains code for generating challenges. A generated challenge is a dict that has two Trials and a type.
"""

from sqlalchemy.sql.functions import random as sql_random
from facelo.trial.models import Trial
from facelo.challenge.models import Challenge
from random import choice, shuffle
from itertools import combinations
from facelo.definitions import (
    CHALLENGE_TYPE_RANDOM,
    CHALLENGE_TYPE_SAMETRIAL,
    CHALLENGE_TYPE_TRIANGLE,
)


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
def generate_challenges(to_create: dict[int, int], completed: list[Challenge]) -> list[Challenge]:
    # I need to check that I dont send the same ones everytime
    # I think I only dont want to send the same ones in the newly created with respect to the last 50.
    generated_random = gen_chall_data_random(size=to_create[CHALLENGE_TYPE_RANDOM])
    generated_sametrial = gen_chall_data_sametrial(to_create[CHALLENGE_TYPE_SAMETRIAL], completed)
    generated_triangle = gen_chall_data_triangle(to_create[CHALLENGE_TYPE_TRIANGLE], completed)
    generated = generated_random + generated_sametrial + generated_triangle

    # TODO test
    # TODO this can be improved
    for combo in combinations(generated, 2):
        if (combo[0]["trial_1"] == combo[1]["trial_1"] and combo[0]["trial_2"]
                == combo[1]["trial_2"]) or (combo[0]["trial_1"] == combo[1]["trial_2"] and
                                            combo[0]["trial_2"] == combo[1]["trial_1"]):
            # Maximum 1 of the combo needs to remain, this is not straightforward.
            if combo[0] in generated:
                generated.remove(combo[0])

    # now checking that they are not the same as completed challs
    # TODO test this
    for chall in completed:
        generated[:] = [
            gen_sample for gen_sample in generated
            if not ((gen_sample["trial_1"] == chall.winner_id and gen_sample["trial_2"] ==
                     chall.loser_id) or (gen_sample["trial_1"] == chall.loser_id and
                                         gen_sample["trial_2"] == chall.winner_id))
        ]
    shuffle(generated)
    return generated


def gen_chall_data_random(size: int) -> list[dict[str, int]]:
    """Returns a list with dictionaries with random trials. From that dictionary a challenge can be generated. If requested number of challenges cant be generated, the maximum possible will be returned."""
    generated = []
    while len(generated) < size:
        trial_1, trial_2 = next(random_trials), next(random_trials)
        if trial_1.image.user == trial_2.image.user:
            size -= 1
            continue
        generated.append({"type": CHALLENGE_TYPE_RANDOM, "trial_1": trial_1, "trial_2": trial_2})
    return generated


def gen_chall_data_sametrial(size: int, completed: list[Challenge]) -> list[dict[str, int]]:
    if random_trials == None or len(completed) == 0:
        return []

    same_trials = [chall.winner for chall in completed if chall.winner
                  ] + [chall.loser for chall in completed if chall.loser]

    generated = []
    while len(generated) < size:
        trial_1 = next(random_trials)
        trial_2 = choice(same_trials)
        if trial_1.image.user == trial_2.image.user:
            size -= 1
            continue
        generated.append({"type": CHALLENGE_TYPE_RANDOM, "trial_1": trial_1, "trial_2": trial_2})
    return generated


def gen_chall_data_triangle(size: int, completed: list[Challenge]) -> list[dict[str, int]]:
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

        if winner.image.user != loser.image.user:
            if choice([True, False]):
                generated.append({
                    "type": CHALLENGE_TYPE_RANDOM,
                    "trial_1": winner,
                    "trial_2": loser
                })
            else:
                generated.append({
                    "type": CHALLENGE_TYPE_RANDOM,
                    "trial_1": loser,
                    "trial_2": winner
                })

        if len(generated) == size:
            break
    return generated
