# coding: utf-8

from marshmallow import Schema, fields, post_load, pre_load


class ChallengeSchema(Schema):
    id = fields.Integer()

    question_id = fields.Integer(dump_only=True)
    winner_id = fields.Integer()
    loser_id = fields.Integer()

    winner_image_url = fields.Url(dump_only=True)
    loser_image_url = fields.Url(dump_only=True)

    @pre_load
    def load(self, data, pass_many=True, **kwargs):
        return data['challenges']



challenge_schema = ChallengeSchema()
challenge_schemas = ChallengeSchema(many=True)
