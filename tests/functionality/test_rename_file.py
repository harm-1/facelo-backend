import os

import pytest
from flask import current_app

from factories.factories import lazy_random_image


def test_save_image():
    lazy_random_image_generator = lazy_random_image()
    filename = next(lazy_random_image_generator)

    assert filename in os.listdir(current_app.config['IMAGES_DIR'])
