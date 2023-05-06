# -*- coding: utf-8 -*-
"""Create an application instance."""
from facelo.app import create_app
from facelo.settings import DevConfig, ProdConfig
import os

CONFIG = DevConfig if os.getenv('FLASK_ENV') == 'development' else ProdConfig

app = create_app(CONFIG)


