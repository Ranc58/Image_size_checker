from marshmallow import Schema, fields


class ImageSchema(Schema):
    url = fields.Url(required=True)
