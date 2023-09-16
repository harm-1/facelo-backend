# coding: utf-8

from marshmallow import Schema, ValidationError, fields, validates_schema


class TrialSchema(Schema):
    id = fields.Integer(dump_only=True)
    score = fields.Float(dump_only=True)
    judge_age_min = fields.Integer()
    judge_age_max = fields.Integer()

    question_id = fields.Integer(dump_only=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["judge_age_min"] >= data["judge_age_max"]:
            raise ValidationError("The minimum judge age must be lower than the maximum judge age.")


trial_schema = TrialSchema()
trial_schemas = TrialSchema(many=True)
