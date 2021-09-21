# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user

from facelo.database import db
from .models import Challenge
from .serializers import challenge_schema, challenge_schemas

blueprint = Blueprint('challenge', __name__)


@blueprint.route('/question/<question_id>/challenges', methods=['GET'])
@jwt_required()
@marshal_with(challenge_schemas)
def get_challenges():
    challenges = generate_challenges()
    return challenges


@blueprint.route('/question/<question_id>/challenges', methods=['PUT'])
@jwt_required()
@use_kwargs(challenge_schemas)
@marshal_with(challenge_schemas)
def put_challenges(**kwargs):
    breakpoint()
    return True

def generate_challenges():
    pass
