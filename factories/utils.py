
# -*- coding: utf-8 -*-
"""factories to help in tests."""
import os
from random import choice

from flask import current_app

from facelo.image.models import Image
from facelo.question.models import Question
from facelo.trial.models import Trial
from facelo.user.models import User
from facelo.utils import _load_image_as_string, save_image


def lazy_users():
    """turn `User.query.all()` into a lazily evaluated generator"""
    while True:
        user_list = User.query.all()
        # yield choice(user_list) if user_list else None
        for user in user_list:
            if user not in User.query.all():
                break
            yield user


def random_image_filename():
    random_image_filename = choice(os.listdir('/facelo/example_images'))
    random_image_filepath = '{}/{}'.format(current_app.config['EXAMPLE_IMAGES_DIR'],
                                           random_image_filename)
    random_image_str = _load_image_as_string(random_image_filepath)
    filename = save_image(random_image_str, random_image_filename)
    return filename


def lazy_images():
    while True:
        # yield choice(Image.query.all())
        for image in Image.query.all():
            if image not in Image.query.all():
                break
            yield image


def lazy_questions():
    while True:
        yield choice(Question.query.all())
        for question in Question.query.all():
            if question not in Question.query.all():
                break
            yield question


def lazy_trials():
    # curr = None
    while True:
        # prev = curr
        # while prev == curr:
        #     curr = choice(Trial.query.all())
        # yield curr
        for trial in Trial.query.all():
            if trial not in Trial.query.all():
                break
            yield trial
