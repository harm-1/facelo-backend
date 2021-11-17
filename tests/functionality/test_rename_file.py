import os

import pytest
from flask import current_app

from factories.factories import lazy_random_image


def test_save_image():
    filename = lazy_random_image()

    assert filename in os.listdir(current_app.config['IMAGES_DIR'])
