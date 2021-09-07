# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class ImageSchema(Schema):
    image_url = fields.Url()
    created = fields.DateTime(dump_only=True)
    date_taken = fields.DateTime()

    # Ik denk niet dat ik hier de user_id moet hebben. Niet voor dump noch load

image_schema = ImageSchema()
image_schemas = ImageSchema(many=True)
