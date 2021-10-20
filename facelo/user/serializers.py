# coding: utf-8

from marshmallow import Schema, fields, post_dump, pre_load


class UserSchema(Schema):
    email = fields.Email()
    password = fields.Str(load_only=True)
    birth_day = fields.Date()
    gender = fields.Integer()
    sexual_preference = fields.Integer()
    karma = fields.Integer()
    token = fields.Str(dump_only=True)


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
