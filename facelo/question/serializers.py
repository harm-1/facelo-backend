# coding: utf-8

from marshmallow import Schema, fields, validates_schema


class QuestionSchema(Schema):
    id = fields.Integer(dump_only=True)
    question = fields.Str()

question_schema = QuestionSchema()
question_schemas = QuestionSchema(many=True)
