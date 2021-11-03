
import pytest
from factories import (
    ChallengeFactory,
    ImageFactory,
    QuestionFactory,
    TrialFactory,
    UserFactory,
)


@pytest.fixture
def users(db, user, request):
    # This fixture uses the user fixture, because I pass data to that fixture. So that
    # I have a user that I can log into
    # I subtract 1 to compensate for the user
    size = request.param if hasattr(request, "param") else 10
    users = UserFactory.create_batch(size=size - 1)
    # I yield the user and the users in one list
    yield [user] + users
    for new_user in users:
        new_user.delete(commit=False)
    db.session.commit()


@pytest.fixture
def images(db, image, request, users):
    size = request.param if hasattr(request, "param") else 20
    images = ImageFactory.create_batch(size=size - 1)
    yield [image] + images
    for new_image in images:
        new_image.delete(commit=False)
    db.session.commit()


@pytest.fixture
def questions(db, question, request):
    size = request.param if hasattr(request, "param") else 1
    questions = QuestionFactory.create_batch(size=size - 1)
    yield [question] + questions
    # I wont remove questions ever for data consistancy
    # So I wont remove them here


@pytest.fixture
def trials(db, trial, request, images, questions):
    size = request.param if hasattr(request, "param") else 20
    trials = TrialFactory.create_batch(size=size - 1)
    yield [trial] + trials
    for new_trial in trials:
        new_trial.delete(commit=False)
    db.session.commit()


@pytest.fixture
def challenges(db, request, users, trials, questions):
    size = request.param if hasattr(request, "param") else 300
    challenges = ChallengeFactory.create_batch(size=size, completed=True)
    yield challenges
    # I wont remove challenges ever for data consistancy
    # So I wont remove them here
