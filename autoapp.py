# -*- coding: utf-8 -*-
"""Create an application instance."""
from facelo.app import create_app
from facelo.settings import DevConfig, ProdConfig
from flask.helpers import get_env

CONFIG = DevConfig if get_env() == "development" else ProdConfig

app = create_app(CONFIG)
