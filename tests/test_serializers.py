import json

import pytest

from facelo.challenge.serializers import ChallengeSchema
from facelo.user.serializers import UserSchema


@pytest.mark.usefixtures("db")
class TestUser:

    def test_dump_userschema(self, user):
        user_json = UserSchema().dumps(user)
        assert type(user_json) is str
        user_dict = json.loads(user_json)
        assert 'password' not in user_dict

    def test_load_userschema(self, user):
        user_json = UserSchema().dumps(user)
        user_dict = json.loads(user_json)
        user_dict['password'] = user.password
        user_dict['terms_accepted'] = True
        user_dict.pop('token')
        user_dict.pop('karma')
        assert UserSchema().load(user_dict)


@pytest.mark.usefixtures("db")
class TestChallenge:

    def test_dump_challengeschema(self, challenge):
        challenge_json = ChallengeSchema().dumps(challenge)
        assert type(challenge_json) is str
        challenge_dict = json.loads(challenge_json)
        assert type(challenge_dict) is dict

    def test_dump_many_challengeschema(self, challenge):
        challenge_json = ChallengeSchema(many=True).dumps([challenge])
        assert type(challenge_json) is str
        challenges_list = json.loads(challenge_json)
        assert type(challenges_list) is list
        assert type(challenges_list[0]['id']) is int
