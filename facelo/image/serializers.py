# coding: utf-8

from marshmallow import Schema, fields, post_dump, pre_dump, pre_load

from facelo.utils import load_image_as_string


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    filename = fields.String()
    file = fields.String()
    created = fields.DateTime(dump_only=True)
    date_taken = fields.DateTime()

    @post_dump
    def load_file(self, data, **kwargs):
        filename = data.pop('filename')
        data['file'] = load_image_as_string(filename)
        return data


image_schema = ImageSchema()
image_schemas = ImageSchema(many=True)
