# coding: utf-8
from marshmallow import Schema, fields, post_dump, post_load, pre_load


# TODO there should be a different schema for user registering
# Now it works, but im afraid it can be dangerous to use the same
# schema for registering and getting a user
class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    terms_accepted = fields.Boolean(required=False, load_only=True)
    birth_day = fields.Date(required=True)
    gender = fields.Integer(required=True)
    sexual_preference = fields.Integer(required=True)
    karma = fields.Integer(dump_only=True)
    token = fields.Str(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        assert data.pop('terms_accepted')
        return data


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    token = fields.Str(dump_only=True)
