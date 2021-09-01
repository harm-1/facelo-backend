# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class ImageSchema(Schema):
    image_url = fields.Url()
    created = fields.DateTime()
    uploaded = fields.DateTime()
    age_in_image = fields.Integer()

    # Ik denk niet dat ik hier de user_id moet hebben. Niet voor dump noch load

image_schema = ImageSchema()
image_schemas = ImageSchema(many=True)
