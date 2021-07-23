# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from datetime import timedelta


class Config(object):
    """Base configuration."""
    # SECRET_KEY = os.environ.get('CONDUIT_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # BCRYPT_LOG_ROUNDS = 13
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    # CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}".format(
        os.environ.get('DATABASE_DIALECT'),
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        os.environ.get('DATABASE_ADDRESS'),
        os.environ.get('MYSQL_DATABASE'))
    # JWT_AUTH_USERNAME_KEY = 'email'
    # JWT_AUTH_HEADER_PREFIX = 'Token'
    # CORS_ORIGIN_WHITELIST = [
        # 'http://0.0.0.0:4100',
        # 'http://localhost:4100',
        # 'http://0.0.0.0:8000',
        # 'http://localhost:8000',
        # 'http://0.0.0.0:4200',
        # 'http://localhost:4200',
        # 'http://0.0.0.0:4000',
        # 'http://localhost:4000',
    # ]
    # JWT_HEADER_TYPE = 'Token'


class ProdConfig(Config):
    """Production configuration."""

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             # 'postgresql://localhost/example')


class DevConfig(Config):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}".format(
        os.environ.get('DATABASE_DIALECT'),
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        os.environ.get('DATABASE_ADDRESS'),
        os.environ.get('MYSQL_DATABASE'))
    SECRET_KEY = 'very-secret'
    # CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}".format(
        os.environ.get('DATABASE_DIALECT'),
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        os.environ.get('DATABASE_ADDRESS'),
        os.environ.get('MYSQL_DATABASE'))
    SECRET_KEY = 'very-secret'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    # BCRYPT_LOG_ROUNDS = 4
