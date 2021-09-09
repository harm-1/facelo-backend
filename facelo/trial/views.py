# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user

from facelo.database import db
from .models import Trial
from facelo.image.models import Image
from .serializers import trial_schema, trial_schemas

blueprint = Blueprint('trial', __name__)


@blueprint.route('/images/<image_id>/trials/', methods=['GET'])
@jwt_required()
@marshal_with(trial_schemas)
def get_trials(image_id):
    return Image.query.filter_by(id=image_id).first().trials


@blueprint.route('/images/<image_id>/trials/<trial_id>', methods=['GET'])
@jwt_required()
@marshal_with(trial_schema)
def get_trial(image_id, trial_id):
    return Image.query.filter_by(id=image_id).first().query.filter_by(id=trial_id).first()


@blueprint.route('/images/<image_id>/trials/', methods=['POST'])
@jwt_required()
@use_kwargs(trial_schema)
@marshal_with(trial_schema)
def create_trial(image_id, **kwargs):
    image = Image.query.filter_by(id=image_id).first()
    return Trial(image=image, **kwargs).save()



@blueprint.route('/images/<image_id>/trials/<trial_id>', methods=['PUT'])
@jwt_required()
@use_kwargs(trial_schema)
@marshal_with(trial_schema)
def update_trial(image_id, trial_id, **kwargs):
    trial = Image.query.filter_by(id=image_id).first().query.filter_by(id=trial_id).first()
    trial.update(**kwargs)
    return trial

