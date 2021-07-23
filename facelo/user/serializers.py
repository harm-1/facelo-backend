# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    token = fields.Str(dump_only=True)
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')

    # @pre_load
    # def make_user(self, data, **kwargs):
    #     print('1')
    #     print(data)
    #     return(data)

    # @post_dump
    # def dump_user(self, data, **kwargs):
    #     print('1')
    #     return {'user': data}


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
