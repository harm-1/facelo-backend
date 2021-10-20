# -*- coding: utf-8 -*-
"""Test configs."""
from facelo.app import create_app
from facelo.settings import DevConfig, ProdConfig

# def test_production_config():
#     """Production config."""
#     app = create_app(ProdConfig)
#     assert app.config['ENV'] == 'production'
#     assert not app.config['DEBUG']


# def test_dev_config():
#     """Development config."""
#     app = create_app(DevConfig)
#     assert app.config['ENV'] == 'development'
#     assert app.config['DEBUG']
