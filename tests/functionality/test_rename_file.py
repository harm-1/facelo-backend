import os

import pytest
from flask import current_app

from factories.factories import random_image_filename


def test_save_image():
    filename = random_image_filename()

    assert filename in os.listdir(current_app.config['IMAGES_DIR'])
