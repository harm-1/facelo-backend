# coding: utf-8

from marshmallow import Schema, fields, post_dump, pre_load


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    filename = fields.String()
    created = fields.DateTime(dump_only=True)
    date_taken = fields.DateTime()


image_schema = ImageSchema()
image_schemas = ImageSchema(many=True)
