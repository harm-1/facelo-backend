# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required

from facelo.database import db

from .models import Question
from .serializers import question_schema, question_schemas

blueprint = Blueprint("question", __name__)


@blueprint.route("/questions/", methods=["GET"])
@jwt_required()
@marshal_with(question_schemas)
def get_questions():
    return Question.query.all()


@blueprint.route("/questions/<question_id>", methods=["GET"])
@jwt_required()
@marshal_with(question_schema)
def get_question(question_id):
    return Question.query.filter_by(id=question_id).first()
