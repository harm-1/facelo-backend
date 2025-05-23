# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound

from facelo.database import db as _db
from facelo.user.models import User
from factories import (ChallengeFactory, ImageFactory, QuestionFactory,
                       TrialFactory, UserFactory)

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
@click.option("--pdb", default=0)
def test(pdb):
    """Run the tests."""
    import pytest

    if pdb:
        rv = pytest.main([TEST_PATH, "--verbose", "--pdb"])
    else:
        rv = pytest.main([TEST_PATH, "--verbose"])
    exit(rv)


@click.command()
@click.option("-f", "--fix-imports", default=False, is_flag=True)
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ["requirements"]
    root_files = glob("*.py")
    root_directories = [name for name in next(os.walk("."))[1] if not name.startswith(".")]
    files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo("{}: {}".format(description, " ".join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool("Fixing import order", "isort", "-rc")
    execute_tool("Checking code style", "flake8")


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, _, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".pyc") or filename.endswith(".pyo"):
                full_pathname = os.path.join(dirpath, filename)
                click.echo("Removing {}".format(full_pathname))
                os.remove(full_pathname)


@click.command()
@click.option("--url", default=None, help="Url to test (ex. /static/image.png)")
@click.option("--order", default="rule", help="Property on Rule to order by")
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.
    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_headers = ("Rule", "Endpoint", "Arguments")

    if url:
        try:
            rule, arguments = current_app.url_map.bind("localhost").match(url, return_rule=True)
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(("<{}>".format(e), None, None))
            column_length = 1
    else:
        rules = sorted(current_app.url_map.iter_rules(), key=lambda rule: getattr(rule, order))
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ""
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += "{:" + str(max_rule_length) + "}"
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        max_endpoint_length = max_endpoint_length if max_endpoint_length > 8 else 8
        str_template += "  {:" + str(max_endpoint_length) + "}"
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = max_arguments_length if max_arguments_length > 9 else 9
        str_template += "  {:" + str(max_arguments_length) + "}"
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo("-" * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))


@click.command()
@click.option("-u", "--users", default=0, type=int)
@click.option("-i", "--images", default=0, type=int)
@click.option("-t", "--trials", default=0, type=int)
@click.option("-q", "--questions", default=0, type=int)
@click.option("-c", "--challenges", default=0, type=int)
@click.option("-e", "--email", default="foo@bar.com", type=str, help="dummy user email")
@click.option("-p", "--password", default="foobar", type=str, help="dummy user pw")
@with_appcontext
def seed(users, images, trials, questions, challenges, email, password):
    print("deleting database")
    assert current_app.debug
    assert current_app.config["ENV"] == "development"
    # I need to have a look into this.
    # I dont want to remove the database when I run the app in debug mode.
    assert os.environ.get("MYSQL_DATABASE") == 'facelo_testing'
    _db.drop_all()

    print("creating database")
    _db.create_all()

    print("seeding database")
    assert trials <= images * questions
    print(f"creating {users} users, {images} images, {trials} trials, "
          f"{questions} questions, {challenges} challenges")

    c_users = []
    if users:
        c_user = UserFactory(email=email, password=password)
        c_users = [c_user] + UserFactory.create_batch(size=users - 1)
    c_images = ImageFactory.create_batch(size=images)
    c_questions = QuestionFactory.create_batch(size=questions)
    c_trials = TrialFactory.create_batch(size=trials)
    c_challenges = ChallengeFactory.create_batch(size=challenges)

    print(f"created {len(c_users)} users, {len(c_images)} images, {len(c_trials)} trials, "
          f"{len(c_questions)} questions, {len(c_challenges)} challenges")
