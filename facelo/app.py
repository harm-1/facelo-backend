# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
# import logging

from flask import Flask

from facelo.exceptions import InvalidUsage
from facelo.extensions import bcrypt, cors, db, jwt, migrate
from facelo.settings import DevConfig, TestConfig, ProdConfig
from facelo import challenge, commands, image, question, trial, user
from flask.app import Flask
from typing import Type, Union


def create_app(config_object=ProdConfig) -> Flask:
    """Create application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    # logger
    return app


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    origins = app.config.get("CORS_ORIGIN_WHITELIST", "*")
    cors.init_app(app, origins=origins)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""

    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(image.views.blueprint)
    app.register_blueprint(trial.views.blueprint)
    app.register_blueprint(question.views.blueprint)
    app.register_blueprint(challenge.views.blueprint)


def register_errorhandlers(app: Flask) -> None:

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app: Flask) -> None:
    """Register shell context objects."""
    pass


def register_commands(app: Flask) -> None:
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.seed)
