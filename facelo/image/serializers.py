# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    image_url = fields.Url()
    created = fields.DateTime(dump_only=True)
    date_taken = fields.DateTime()


image_schema = ImageSchema()
image_schemas = ImageSchema(many=True)
