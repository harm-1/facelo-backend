# -*- coding: utf-8 -*-
import datetime as dt
from collections import Counter

from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required

from facelo.database import db

from .models import Challenge
from .serializers import challenge_schema, challenge_schemas
from .generate import generate_challenges

blueprint = Blueprint("challenge", __name__)

from facelo.question.models import Question

from facelo.definitions import (
    CHALLENGE_TYPE_RANDOM,
    CHALLENGE_TYPE_SAMETRIAL,
    CHALLENGE_TYPE_TRIANGLE,
)


@blueprint.route("/question/<question_id>/challenges", methods=["GET"])
@jwt_required()
@marshal_with(challenge_schemas)
def get_challenges(question_id: int):
    question = Question.get_by_id(question_id)
    challenges = get_latest_challenges(question, 62)
    completed, uncompleted = sort_by_completed(challenges)

    # check 12 unfullfilled
    if len(uncompleted) > 12:
        return uncompleted

    to_create = generate_challenges_type(len(uncompleted))
    generated = generate_challenges(to_create, completed)
    created = create_challenges(generated, question)

    return uncompleted + created


@blueprint.route("/question/<question_id>/challenges", methods=["PUT"])
@jwt_required()
@use_kwargs(challenge_schemas)
@marshal_with(challenge_schemas)
def put_challenges(*challenges, **kwargs):
    for chall_result in challenges:
        chall_ori = Challenge.get_by_id(chall_result["id"]).complete(chall_result)

    return ("", 204)


def get_latest_challenges(question: Question, size=62) -> list[Challenge]:
    latest = (Challenge.query.filter_by(judge=current_user, question_id=question.id).order_by(
        Challenge.id.desc()).limit(size).all())
    return latest


def sort_by_completed(challenges: list[Challenge]):
    completed = []
    uncompleted = []
    for challenge in challenges:
        if challenge.completed:
            completed.append(challenge)
        else:
            uncompleted.append(challenge)
    return completed, uncompleted


def generate_challenges_type(uncompletedCount: int) -> dict[int, int]:
    to_create = {}
    if uncompletedCount < 6:
        to_create = {
            CHALLENGE_TYPE_RANDOM: 6,
            CHALLENGE_TYPE_SAMETRIAL: 4,
            CHALLENGE_TYPE_TRIANGLE: 2,
        }
    elif uncompletedCount < 12:
        to_create = {
            CHALLENGE_TYPE_RANDOM: 3,
            CHALLENGE_TYPE_SAMETRIAL: 2,
            CHALLENGE_TYPE_TRIANGLE: 1,
        }
    return to_create


def create_challenges(generated: list[dict[str, int]], question: Question):
    # Now the challenges are created, it is done this way to create them in random order
    created = []
    for gen_sample in generated:
        created.append(
            Challenge(
                judge=current_user,
                judge_age=None,
                type=gen_sample["type"],
                question=question,
                winner=gen_sample["trial_1"],
                loser=gen_sample["trial_2"],
            ))
    db.session.commit()
    return created
